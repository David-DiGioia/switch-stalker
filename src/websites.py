from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import logger
from selenium.webdriver import ActionChains

button_online_html = '<button data-test="shippingATCButton" type="button" class="Button-bwu3xu-0 defxwW">Ship it</button>'
button_online_css = "button[data-test='shippingATCButton'][type='button'][class='Button-bwu3xu-0 defxwW']"
no_button_online_css = "div[data-test='oosDeliveryOption'][class='h-text-orangeDark h-text-md']"
decline_coverage_button_css = "button[data-test='espModalContent-declineCoverageButton'][type='button'][class='Button-bwu3xu-0 ciMIqu h-margin-t-tight']"

email = ''
password = ''


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
    def __init__(self, url, online):
        self.url = url
        if online:
            self.purchase_button_html = button_online_html
            self.purchase_button_css = button_online_css
        else:
            self.purchase_button_html = ''
            self.purchase_button_css = ''

    def in_stock(self, driver, timeout):
        driver.get(self.url)
        if wait_css(self.purchase_button_css, driver, timeout):
            return self.purchase_button_html in driver.page_source
        return False

    def add_to_cart(self, driver, timeout):
        wait_click_css(self.purchase_button_css, driver, timeout)

    def checkout(self):
        pass

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

        # We hold and click the login button so hopefully it doesn't block us for being a bot
        login_button = wait_css('#login', driver, timeout)
        actions = ActionChains(driver)
        actions.move_to_element(login_button).click_and_hold(login_button).perform()
        actions.click().perform()

        time.sleep(1000000)
