from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logger
import options
import pickle

button_online_html = '<button data-test="shippingATCButton" type="button" class="Button-bwu3xu-0 defxwW">Ship it</button>'
button_online_css = "button[data-test='shippingATCButton'][type='button'][class='Button-bwu3xu-0 defxwW']"
no_button_online_css = "div[data-test='oosDeliveryOption'][class='h-text-orangeDark h-text-md']"
select_address_html = 'label[class="h-display-block h-position-relative"][data-test="ba9bdaa0-8350-11ea-9dc1-0313c1f58d21"]'


# Wait for css element to be clickable then return the element. Return None if timeout occurs.
def wait_css(css, driver, timeout, task_id):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    except TimeoutException:
        logger.log(f"Timed out waiting for css element to be clickable: {css}", task_id)
        return None
    except Exception as e:
        logger.log_exception(e, task_id)
        return None
    return driver.find_element_by_css_selector(css)


# Wait for css element to be clickable then click it. Returns True if element is successfully clicked.
def wait_click_css(css, driver, timeout, task_id):
    element = wait_css(css, driver, timeout, task_id)
    if element is not None:
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            logger.log_exception(e, task_id)
            return None
        return element
    return None


# If element is found, return it. Otherwise, return None.
def immediate_active_css(css, driver, task_id):
    try:
        element = driver.find_element_by_css_selector(css)
    except NoSuchElementException:
        return None
    except Exception as e:
        logger.log_exception(e, task_id)
        return None
    if element.is_displayed() and element.is_enabled():
        return element
    return None


class Target:
    def __init__(self, url, online=True):
        self.name = 'Target'
        self.url = url
        if online:
            self.purchase_button_html = button_online_html
            self.purchase_button_css = button_online_css
            self.no_purchase_button_css = no_button_online_css
        else:
            self.purchase_button_html = ''
            self.purchase_button_css = ''
            self.no_purchase_button_css = ''

    def in_stock(self, driver, timeout, task_id):
        if wait_css(self.purchase_button_css + ', ' + self.no_purchase_button_css, driver, timeout, task_id):
            return self.purchase_button_html in driver.page_source
        return False

    def add_to_cart(self, driver, timeout, task_id):
        # Click purchase button
        wait_click_css(self.purchase_button_css, driver, timeout, task_id)
        # Exit from popup
        wait_click_css('button[aria-label="close"][type="button"][style="position: absolute; top: 5px; right: 5px;"]', driver, timeout, task_id)
        wait_click_css('#cart', driver, timeout, task_id)

    # Checkout once we know what information is already filled out for us.
    def checkout_starting_from(self, step, driver, timeout, task_id):
        # Choose address
        if step <= 0:
            # Select the address
            wait_click_css(select_address_html, driver, timeout, task_id)
            # Save and continue
            wait_click_css('[data-test="save-and-continue-button"][type="button"][class="Button-bwu3xu-0 hYDopb"]', driver, timeout, task_id)

        # Enter credit card number
        if step <= 1:
            # Click box and enter credit card number
            ccn_input_box = wait_click_css('#creditCardInput-cardNumber', driver, timeout, task_id)
            ccn_input_box.send_keys(options.ccn)
            # Click 'confirm card' button
            wait_click_css('button[data-test="verify-card-button"][type="button"][class="Button-bwu3xu-0 hYDopb"]', driver, timeout, task_id)

        # Enter security code
        if step <= 2:
            # Click box and enter credit card number
            sc_input_box = wait_click_css('#creditCardInput-cvv', driver, timeout, task_id)
            sc_input_box.send_keys(options.sc)
            # <button data-test="save-and-continue-button" type="button" class="Button-bwu3xu-0 hYDopb">
            wait_click_css('button[data-test="save-and-continue-button"][type="button"][class="Button-bwu3xu-0 hYDopb"]', driver, timeout, task_id)

        # Make the purchase!!!
        final_button = wait_css('button[class="Button__ButtonWithStyles-y45r97-0 eYxNTC"][data-test="placeOrderButton"]', driver, timeout, task_id)
        if final_button is None:
            logger.log("Failed at final button.", task_id)
            return False
        if options.debug:
            logger.log(f"This is where we would check out. Button is: {final_button}", task_id)
        else:
            # Executing script directly instead of clicking to hopefully
            # avoid getting selenium.common.exceptions.ElementClickInterceptedException
            driver.execute_script("arguments[0].click();", final_button)
            logger.log(f"SUCCESSFUL PURCHASE AT {self.url}", task_id)
        return True

    # Make the purchase. Returns true if successful.
    def checkout(self, driver, timeout, task_id):
        # Click 'I'm ready to checkout' button
        if wait_click_css('button[class="Button__ButtonWithStyles-y45r97-0 gmmYfU"][data-test="checkout-button"]', driver, timeout, task_id) is None:
            return False

        while True:
            # Select address
            if immediate_active_css(select_address_html, driver, task_id) is not None:
                logger.log("Checking out from stage 0 (address).", task_id)
                return self.checkout_starting_from(0, driver, timeout, task_id)

            # Enter credit card number
            if immediate_active_css('#creditCardInput-cardNumber', driver, task_id) is not None:
                logger.log("Checking out from stage 1 (credit card number).", task_id)
                return self.checkout_starting_from(1, driver, timeout, task_id)

            # Do security code here
            if immediate_active_css('#creditCardInput-cvv', driver, task_id) is not None:
                logger.log("Checking out from stage 2 (security code).", task_id)
                return self.checkout_starting_from(2, driver, timeout, task_id)

            # Check for final button
            if immediate_active_css('button[class="Button__ButtonWithStyles-y45r97-0 eYxNTC"][data-test="placeOrderButton"]', driver, task_id):
                logger.log("Checking out from stage 3 (Place order button).", task_id)
                return self.checkout_starting_from(3, driver, timeout, task_id)

    def login(self, driver, timeout, task_id):
        driver.get(self.url)
        logger.log(f"Loading cookies...", task_id)
        for cookie in pickle.load(open("Cookies.pkl", "rb")):
            driver.add_cookie(cookie)
        logger.log("Finished loading cookies.", task_id)


class SmythsToys:
    def __init__(self, url, online=True):
        self.name = 'SmythsToys'
        self.url = url

    def in_stock(self, driver, timeout, task_id):
        add_to_basket_button = wait_css('#addToCartButton', driver, 5, task_id)
        return add_to_basket_button is not None

    def add_to_cart(self, driver, timeout, task_id):
        # Click purchase button
        wait_click_css('#addToCartButton', driver, timeout, task_id)
        # Go to cart
        wait_click_css('#showCartPopup', driver, timeout, task_id)

    # Checkout once we know what information is already filled out for us.
    def checkout_starting_from(self, step, driver, timeout, task_id):
        pass

    # Make the purchase. Returns true if successful.
    def checkout(self, driver, timeout, task_id):
        wait_click_css('#checkoutOnCart', driver, timeout, task_id)
        input_box = wait_click_css('#cardNumberPart1', driver, timeout, task_id)
        input_box.send_keys(options.ccn)
        input_box = wait_click_css('#cardCvn', driver, timeout, task_id)
        input_box.send_keys(options.sc)
        # Select month
        wait_click_css('button[type="button"][class="btn dropdown-toggle selectpicker contact_select"][data-toggle="dropdown"][data-id="expiryMonth"]', driver, timeout, task_id)
        wait_click_css('li[rel="' + str(int(options.month)) + '"]', driver, timeout, task_id)
        # Select Year
        wait_click_css('button[type="button"][class="btn dropdown-toggle selectpicker contact_select"][data-toggle="dropdown"][data-id="expiryYear"]', driver, timeout, task_id)
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.LINK_TEXT, "20" + options.year[:-1])))
        element.click()
        # wait_click_css('label[class="control control--checkbox fnt_12"]', driver, timeout, task_id)
        agree_button = driver.find_elements_by_xpath("//*[contains(text(), 'By placing the order, I have read and agreed to the')]")
        agree_button[0].click()

        if options.debug:
            logger.log("This is where we would checkout", task_id)
            return True
        else:
            logger.log("Placing order", task_id)
            wait_click_css('#placeOrder', driver, timeout, task_id)
            return True

    def login(self, driver, timeout, task_id):
        driver.get('https://www.smythstoys.com/uk/en-gb/login')
        input_box = wait_click_css('#j_username', driver, timeout, task_id)
        input_box.send_keys(options.email)
        input_box = wait_click_css('#j_password', driver, timeout, task_id)
        input_box.send_keys(options.password)
        wait_click_css('button[type="submit"][class="btn btn-blue margn_tp_bt_20"]', driver, timeout, task_id)
        driver.get(self.url)
