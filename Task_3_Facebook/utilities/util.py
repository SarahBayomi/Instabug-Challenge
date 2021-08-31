"""
@package utilities

Util class implementation
All most commonly used utilities should be implemented in this class

Example:
    name = self.util.getUniqueName()
"""
import time
import traceback
import random, string
import utilities.custom_logger as cl
import logging
import re
from traceback import print_stack
from datetime import datetime
import os

class Util(object):

    log = cl.customLogger(logging.INFO)

    def sleep(self, sec, info=""):
        """
        Put the program to wait for the specified amount of time
        """
        if info is not None:
            self.log.info("Wait :: '" + str(sec) + "' seconds for " + info)
        try:
            time.sleep(sec)
        except InterruptedError:
            traceback.print_stack()

    def getAlphaNumeric(self, length, type='letters'):
        """
        Get random string of characters

        Parameters:
            length: Length of string, number of characters string should have
            type: Type of characters string should have. Default is letters
            Provide lower/upper/digits for different types
        """
        alpha_num = ''
        if type == 'lower':
            case = string.ascii_lowercase
        elif type == 'upper':
            case = string.ascii_uppercase
        elif type == 'digits':
            case = string.digits
        elif type == 'mix':
            case = string.ascii_letters + string.digits
        else:
            case = string.ascii_letters
        return alpha_num.join(random.choice(case) for i in range(length))

    def getUniqueName(self, charCount=10):
        """
        Get a unique name
        """
        return self.getAlphaNumeric(charCount, 'lower')

    def getUniqueNameList(self, listSize=5, itemLength=None):
        """
        Get a list of valid email ids

        Parameters:
            listSize: Number of names. Default is 5 names in a list
            itemLength: It should be a list containing number of items equal to the listSize
                        This determines the length of the each item in the list -> [1, 2, 3, 4, 5]
        """
        nameList = []
        for i in range(0, listSize):
            nameList.append(self.getUniqueName(itemLength[i]))
        return nameList

    def verifyTextContains(self, actualText, expectedText):
        """
        Verify actual text contains expected text string

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From test data --> :: " + expectedText)
        if expectedText.lower() in actualText.lower():
            self.log.info("### VERIFICATION CONTAINS !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT CONTAIN!!!")
            return False

    def verifyTextInList(self, actualText, expectedList):
        expectedList = [expectedText.lower() for expectedText in expectedList]
        actualText = actualText.lower()
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("The list in test data --> :: ")
        self.log.info(expectedList)
        if actualText.lower() in expectedList:
            index =expectedList.index(actualText.lower())
            self.log.info("### VERIFICATION LIST CONTAINS !!!")
            return index
        else:
            self.log.info("### VERIFICATION LIST DOES NOT CONTAIN!!!")
            return False

    def verifyTextMatch(self, actualText, expectedText):
        """
        Verify text match

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text From test data --> :: " + expectedText)
        if actualText.lower() == expectedText.lower():
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCH!!!")
            return False

    def verifyTextRegex(self, actualText, expectedText):
        """
        Verify text regex match

        Parameters:
            expectedList: Expected Text
            actualList: Actual Text
        """
        if actualText is None:
            actualText = "NO Actual Text"
        if expectedText is None:
            expectedText = "NO Expected Text"

        self.log.info("Actual Text From Application Web UI --> :: " + actualText)
        self.log.info("Expected Text Regex From test data --> :: " + expectedText)
        actualText = actualText.lower()
        expectedText = expectedText.lower()
        if re.findall(expectedText, actualText):
            self.log.info("### VERIFICATION MATCHED !!!")
            return True
        else:
            self.log.info("### VERIFICATION DOES NOT MATCH!!!")
            return False

    def verifyListMatch(self, expectedList, actualList):
        """
        Verify two list matches

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        return set(expectedList) == set(actualList)

    def verifyListContains(self, expectedList, actualList):
        """
        Verify actual list contains elements of expected list

        Parameters:
            expectedList: Expected List
            actualList: Actual List
        """
        length = len(expectedList)
        for i in range(0, length):
            if expectedList[i] not in actualList:
                return False
        else:
            return True


    def splitUserInput(self, userInput, splittedPart):
        self.log.info("User input is: " + userInput)
        userInput= userInput.split(splittedPart)
        afterSplit = userInput[1]
        self.log.info("User input after splitting is: " + afterSplit)
        return afterSplit

    def cleanseURL(self, url):
        self.log.info("URL to be cleansed is: " + url)
        url = url.replace("%20", " ")
        return url

    def create_dateFileName(self, specifyDateTime, addtionalName):
        #'%d_%m_%Y_%I_%M_%p'
        fileName = datetime.now().strftime(specifyDateTime) + addtionalName
        return fileName

    def createDirectory(self, fileName, folderName):
        Directory = folderName
        relativeFileName = Directory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFileName)
        detinationDirectory = os.path.join(currentDirectory, Directory)

        try:
            if not os.path.exists(detinationDirectory):
                os.makedirs(detinationDirectory)
            time.sleep(5)
            self.log.info("File is saved to directory: " + destinationFile)
            return detinationDirectory
        except:
            self.log.info("### Exception Occurred")
            print_stack()
