import utilities.custom_logger as cl
import logging
from base.basepage import BasePage

class LoginPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super(LoginPage, self).__init__(driver)
        self.driver = driver

    #Locators
    _email_field = '//input[@name="UserName" and @type="email"]'
    _password_field = '//input[@name="Password" and @type="password"]'
    _login_button = '//span[@id="submitButton" and text()="Sign in"]'
    _domain = '//a[contains(., "I have an IT issue or request")]'

    def enterEmail(self, email):
        self.waitForElement(self._email_field, locatorType="xpath")
        self.sendKeys(email, self._email_field, locatorType="xpath")

    def enterPassword(self, password):
        self.waitForElement(self._password_field, locatorType="xpath")
        self.sendKeys(password, self._password_field, locatorType="xpath")

    def clickLoginButton(self):
        self.elementCLick(self._login_button, locatorType="xpath")

    def login(self, email, password):
        self.enterEmail(email)
        self.enterPassword(password)
        self.clickLoginButton()

    def verifyLoginSuccessful(self):
        self.waitForElement(self._domain, locatorType="xpath")
        result = self.isElementPresent(self._domain, locatorType="xpath")
        self.elementCLick(self._domain, locatorType="xpath")
        return result


