from selenium import webdriver

class Task:
    def __init__(self, website, sleep_seconds=5, timeout=10):
        self.website = website
        self.sleep_seconds = sleep_seconds
        self.timeout = timeout
        self.driver = webdriver.Firefox(executable_path="../lib/geckodriver")
        website.login(self.driver, timeout)

    def close(self):
        self.driver.close()
