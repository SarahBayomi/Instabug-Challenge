from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import utilities.custom_logger as cl
import logging
from datetime import datetime
import os
from selenium.webdriver.common.keys import Keys
import pyperclip
import re

class SeleniumDriver():

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def screenShot(self, resultMessage):

        fileName = resultMessage + "." + datetime.now().strftime('%d_%m_%Y_%I_%M_%p') +".png"
        screenShotDirectory = "../screenshots/"
        relativeFileName = screenShotDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile= os.path.join(currentDirectory, relativeFileName)
        detinationDirectory = os.path.join(currentDirectory, screenShotDirectory)

        try:
            if not os.path.exists(detinationDirectory):
                os.makedirs(detinationDirectory)
            self.driver.implicitly_wait(1)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshot is saved to directory: " + destinationFile)
            return True
        except:
            self.log.info("### Exception Occurred")
            print_stack()
            return False

    def savePage(self, appName, actionType):
        element = self.getElement('html', 'css')
        self.driver.implicitly_wait(5)
        element.send_keys(self.getKeyboardKeys() + 'a')
        element.send_keys(self.getKeyboardKeys() + 'c')
        actionType = re.sub('[\s|\W]', '_', actionType)
        fileName = datetime.now().strftime('%d_%m_%Y_%I_%M_%p') + "_" + appName + "_" + actionType + ".txt"
        chatDirectory = "../chats/"
        relativeFileName = chatDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        detinationDirectory = os.path.join(currentDirectory, chatDirectory)

        try:
            if not os.path.exists(detinationDirectory):
                os.makedirs(detinationDirectory)
            self.driver.implicitly_wait(1)
            f = open(destinationFile, "w")
            f.write(pyperclip.paste())
            f.close()
            self.log.info("Chat is saved to directory: " + destinationFile)
        except:
            self.log.info("### Exception Occurred ... Chat is not saved may be there is special characters in the name")
            print_stack()

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "classname":
            return By.CLASS_NAME
        elif locatorType == "linktext":
            return By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator + " and locatorType: " + locatorType)
        return element

    def elementCLick(self, locator="", locatorType ="id", element=None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Cannot click on the element with locator: " + locator + " and locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator, locatorType):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data: " + data + " :on element with locator: " + locator + " and locatorType: " + locatorType)
        except:
            self.log.info("Cannot send: " + data + " :on the element with locator: " + locator + " and locatorType: " + locatorType)
            print_stack()

    def isElementPresent(self, locator, locatorType="id", element= None):
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            if element is not None:
                #self.log.info("Element Found with locator: " + locator + " and locatorType: " + locatorType)
                return True
            else:
                #self.log.info("Element not found with locator: " + locator + " and locatorType: " + locatorType)
                return False
        except:
            self.log.info("Element not found")
            return False

    def elementPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType, timeout=120):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, 120, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,
                                                     ElementNotSelectableException])

            element = wait.until(EC.element_to_be_clickable((self.getElement(locator, locatorType))))
            self.log.info("Element with locator " + locator + " appeared on the web page")
        except:
            self.log.info("Element with locator " + locator + " not appeared on the web page")
            print_stack()
        return element

    def getTitle(self):
        return self.driver.title

    def getText(self, locator="", locatorType="id", element=None, info=""):
        """
        NEW METHOD
        Get 'Text' on an element
        Either provide element or a combination of locator and locatorType
        """
        try:
            if locator: # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            text = element.text
            if len(text) == 0:
                text = element.get_attribute("innerText")
            if len(text) != 0:
                self.log.info("Getting text on element :: " + info)
                self.log.info("The text is :: '" + text + "'")
                text = text.strip()
        except:
            self.log.error("Failed to get text on element " + info)
            print_stack()
            text = None
        return text

    def isElementDisplayed(self, locator="", locatorType="id", element=None):
        """
        NEW METHOD
        Check if element is displayed
        Either provide element or a combination of locator and locatorType
        """
        isDisplayed = False
        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed" )
            else:
                self.log.info("Element not displayed")
            return isDisplayed
        except:
            print("Element not found")
            return False

    def webScroll(self, direction="up"):
        """
        NEW METHOD
        """
        if direction == "up":
            # Scroll Up
            self.driver.execute_script("window.scrollBy(0, -1000);")

        if direction == "down":
            # Scroll Down
            self.driver.execute_script("window.scrollBy(0, 1000);")

    def isElementEnabled(self, locator="", locatorType="id", element=None):
        isEnabled = False

        try:
            if locator:  # This means if locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                isEnabled = element.is_enabled()
                self.log.info("Element is enabled")
            else:
                self.log.info("Element not enabled")
            return isEnabled
        except:
            print("Element not found")
            return False

    def getKeyboardKeys(self):
        return Keys.CONTROL

    def waitElementPresence(self, locator, locatorType, timeout=200):
        element = None
        try:
            self.log.info("Waiting for maximum :: " + str(timeout) + " :: seconds for element to be present")
            wait = WebDriverWait(self.driver, timeout, poll_frequency=1,
                                 ignored_exceptions=[NoSuchElementException, ElementNotVisibleException,
                                                     ElementNotSelectableException])

            element = wait.until(EC.presence_of_element_located((self.getElement(locator, locatorType))))
            self.log.info("Element with locator " + locator + " is present on the web page")
        except:
            self.log.info("Element with locator " + locator + " is not present on the web page")
            print_stack()
        return element