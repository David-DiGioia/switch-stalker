from selenium import webdriver
import pickle
import logger
import time
import threading

rewrite_cookies = False
thread_id = 0

class Task:
    def __init__(self, website, sleep_time=1, timeout=10):
        global thread_id
        thread_id += 1
        self.id = thread_id
        self.website = website
        self.sleep_time = sleep_time
        self.timeout = timeout
        self.driver = webdriver.Firefox(executable_path="../lib/geckodriver")

        # We load the cookies so that we'll be logged in
        self.driver.get(website.url)

        if rewrite_cookies:
            logger.log("Enter something to continue", self.id)
            input()
            logger.log("continuing....", self.id)
            pickle.dump(self.driver.get_cookies(), open("Cookies.pkl", "wb"))
            logger.log("Finished storing cookies.", self.id)
            time.sleep(10000)
        else:
            for cookie in pickle.load(open("Cookies.pkl", "rb")):
                logger.log(f"Loading cookie {cookie}", self.id)
                self.driver.add_cookie(cookie)

    def main_loop(self):
        while True:
            if not self.website.in_stock(self.driver, self.timeout, self.id):
                logger.log(f"{self.website.name} is out of stock. Retrying.", self.id)
                time.sleep(self.sleep_time)
                self.driver.get(self.website.url)
                continue
            logger.log(f"{self.website.name} is in stock!", self.id)
            self.website.add_to_cart(self.driver, self.timeout, self.id)
            if self.website.checkout(self.driver, self.timeout, self.id):
                logger.log(f"Purchase successful from {self.website.url}", self.id)
                break

    def start(self):
        logger.log(f"Task {self.id} started!", self.id)
        t = threading.Thread(target=self.main_loop)
        t.start()

    def close(self):
        self.driver.close()
