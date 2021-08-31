from selenium import webdriver
import utilities.custom_logger as cl
import logging


class WebDriverFactory():
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, browser):

        self.browser = browser

    def getWebDriverInstance(self, URL):

        if self.browser == "ie":
            driver = webdriver.Ie()

        elif self.browser == "firefox":
            driver = webdriver.Firefox()

        elif self.browser == "chrome":
            driver = webdriver.Chrome()

        else:
            driver = webdriver.Firefox()

        self.log.info("Browser used: " + self.browser)
        driver.maximize_window()
        driver.implicitly_wait(30)
        driver.get(URL)
        return driver

