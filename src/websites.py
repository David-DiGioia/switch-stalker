from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logger
import options

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
    return driver.find_element_by_css_selector(css)


# Wait for css element to be clickable then click it. Returns True if element is successfully clicked.
def wait_click_css(css, driver, timeout, task_id):
    element = wait_css(css, driver, timeout, task_id)
    if element is not None:
        element.click()
        return element
    return None


# If element is found, return it. Otherwise, return None.
def immediate_active_css(css, driver):
    try:
        element = driver.find_element_by_css_selector(css)
    except NoSuchElementException:
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
            final_button.click()
            logger.log(f"SUCCESSFUL PURCHASE AT {self.url}", task_id)
        return True

    # Make the purchase. Returns true if successful.
    def checkout(self, driver, timeout, task_id):
        # Click 'I'm ready to checkout' button
        if wait_click_css('button[class="Button__ButtonWithStyles-y45r97-0 gmmYfU"][data-test="checkout-button"]', driver, timeout, task_id) is None:
            return False

        while True:
            # Select address
            if immediate_active_css(select_address_html, driver) is not None:
                logger.log("Checking out from stage 0 (address).", task_id)
                return self.checkout_starting_from(0, driver, timeout, task_id)

            # Enter credit card number
            if immediate_active_css('#creditCardInput-cardNumber', driver) is not None:
                logger.log("Checking out from stage 1 (credit card number).", task_id)
                return self.checkout_starting_from(1, driver, timeout, task_id)

            # Do security code here
            if immediate_active_css('#creditCardInput-cvv', driver) is not None:
                logger.log("Checking out from stage 2 (security code).", task_id)
                return self.checkout_starting_from(2, driver, timeout, task_id)

            # Check for final button
            if immediate_active_css('button[class="Button__ButtonWithStyles-y45r97-0 eYxNTC"][data-test="placeOrderButton"]', driver):
                logger.log("Checking out from stage 3 (Place order button).", task_id)
                return self.checkout_starting_from(3, driver, timeout, task_id)

    # Logging in automatically makes target suspicious so we use cookies now.
    # [Deprecated]
    def login(self, driver, timeout, task_id):
        email = ''
        password = ''
        driver.get('https://www.target.com/')
        # Click the account menu button
        wait_click_css('.AccountLink__SvgUserWrapper-gx13jw-0.btJnUL', driver, timeout, task_id)
        # Click the link to the sign-in page
        wait_click_css('a[href=""][class="Link-sc-1khjl8b-0 NavigationLink-kfyxgv-0 cTwyXB"][data-test="navigation-link"]', driver, timeout, task_id)
        # Enter credentials
        input_box = wait_click_css('#username', driver, timeout, task_id)
        input_box.send_keys(email)
        input_box = wait_click_css('#password', driver, timeout, task_id)
        input_box.send_keys(password)
        # Click checkbox to stay signed in
        wait_click_css('div[for="keep-me-signed-in"][class="Checkbox__CheckboxVisual-n6heu6-5 eASAwe"]', driver, timeout, task_id)
        wait_click_css('#login', driver, timeout, task_id)

