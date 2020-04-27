from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logger

button_online_html = '<button data-test="shippingATCButton" type="button" class="Button-bwu3xu-0 defxwW">Ship it</button>'
button_online_css = "button[data-test='shippingATCButton'][type='button'][class='Button-bwu3xu-0 defxwW']"
no_button_online_css = "div[data-test='oosDeliveryOption'][class='h-text-orangeDark h-text-md']"
decline_coverage_button_css = "button[data-test='espModalContent-declineCoverageButton'][type='button'][class='Button-bwu3xu-0 ciMIqu h-margin-t-tight']"

email = ''
password = ''
ccn = ''
sc = ''


# Wait for css element to be clickable then return the element. Return None if timeout occurs.
def wait_css(css, driver, timeout):
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css)))
    except TimeoutException:
        logger.log(f"Timed out waiting for css element to be clickable: {css}")
        return None
    return driver.find_element_by_css_selector(css)


# Wait for css element to be clickable then click it. Returns True if element is successfully clicked.
def wait_click_css(css, driver, timeout):
    element = wait_css(css, driver, timeout)
    if element is not None:
        element.click()
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

    def in_stock(self, driver, timeout):
        if wait_css(self.purchase_button_css + ', ' + self.no_purchase_button_css, driver, timeout):
            return self.purchase_button_html in driver.page_source
        return False

    def add_to_cart(self, driver, timeout):
        # Click purchase button
        wait_click_css(self.purchase_button_css, driver, timeout)
        # Exit from popup
        wait_click_css('button[aria-label="close"][type="button"][style="position: absolute; top: 5px; right: 5px;"]', driver, timeout)
        wait_click_css('#cart', driver, timeout)

    # Make the purchase. Returns true if successful.
    def checkout(self, driver, timeout):
        # Click 'I'm ready to checkout' button
        if wait_click_css('button[class="Button__ButtonWithStyles-y45r97-0 gmmYfU"][data-test="checkout-button"]', driver, timeout) is None:
            return False

        # # Select address
        # wait_click_css('label[class="h-display-block h-position-relative"][data-test="ba9bdaa0-8350-11ea-9dc1-0313c1f58d21"]', driver, timeout)
        # # Save and continue
        # wait_click_css('[data-test="save-and-continue-button"][type="button"][class="Button-bwu3xu-0 hYDopb"]', driver, timeout)

        final_button = wait_css('button[class="Button__ButtonWithStyles-y45r97-0 eYxNTC"][data-test="placeOrderButton"]', driver, timeout)
        if final_button is None:
            return False
        logger.log(f"This is where we would check out. Button is: {final_button}")
        return True


    # Logging in automatically makes target suspicious so we use cookies now.
    def login(self, driver, timeout):
        driver.get('https://www.target.com/')
        # Click the account menu button
        wait_click_css('.AccountLink__SvgUserWrapper-gx13jw-0.btJnUL', driver, timeout)
        # Click the link to the sign-in page
        wait_click_css('a[href=""][class="Link-sc-1khjl8b-0 NavigationLink-kfyxgv-0 cTwyXB"][data-test="navigation-link"]', driver, timeout)
        # Enter credentials
        input_box = wait_click_css('#username', driver, timeout)
        input_box.send_keys(email)
        input_box = wait_click_css('#password', driver, timeout)
        input_box.send_keys(password)
        # Click checkbox to stay signed in
        wait_click_css('div[for="keep-me-signed-in"][class="Checkbox__CheckboxVisual-n6heu6-5 eASAwe"]', driver, timeout)
        wait_click_css('#login', driver, timeout)

