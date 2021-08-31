import os
from time import sleep
import utilities.custom_logger as cl
import logging
from base.basepage import BasePage
from pages import appfile_read
from utilities import excel_write_data
from utilities import excel_read_data
from utilities.util import Util
import re
from traceback import print_stack

class ChatPage(BasePage):

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super(ChatPage, self).__init__(driver)
        self.driver = driver
        self.util = Util()

    #Locators
    _bubble = '//div[@class="message-chat transition-done message-chat--amelia"][{0}]/div[1]'
    _button = '//div[contains(@id,"{0}")]'
    _text = '//textarea[contains(@class, "ChatInput__input")]'
    _text_submit = '//button[@type="submit"]'
    _upload_button = '//div[@class="dropzone"]/div[@class="dropzone-container"]/input[@type="file"]'

    def getBubble(self, bubbleCount):
        self.waitForElement(self._bubble.format(bubbleCount), locatorType="xpath")
        bubble = self.getText(self._bubble.format(bubbleCount), locatorType="xpath")
        if bubble:
            return bubble
        else:
            return False

    def getChatFile(self, epic, url):
        if epic == "epic_ACD":
            if url is False:
                chatFile = os.getcwd() + "\\Epic_ACD_chat.xlsx"
            else:
                chatFile = os.getcwd() + "\\Epic_ACD_chat_url.xlsx"
        elif epic == "epic_AE":
            chatFile = os.getcwd() + "\\Epic_AE_chat.xlsx"
        elif epic == "epic_X":
            chatFile = os.getcwd() + "\\Epic_X_chat.xlsx"
        else:
            chatFile = " "
            self.log.info("No chat file for this key phrase!!")

        self.log.info("Epic name is: " + epic + " and chat file used is: " + str(chatFile))
        return chatFile

    def readChatFile(self, chatFile, chatFile_row, chatFile_col):
        chatOutput = excel_read_data.readFile(chatFile, chatFile_row, chatFile_col)
        return chatOutput

    def compareChat(self, tobiLemma, bubble):
        result = self.util.verifyTextRegex(bubble, tobiLemma)
        return result

    def buttons(self, userInput):
        userLemma = self.util.splitUserInput(userInput, "Button_")
        self.waitForElement(self._button.format(userLemma), locatorType="xpath")
        self.elementCLick(self._button.format(userLemma), locatorType="xpath")

    def upload(self):
        sleep(5)
        self.sendKeys(os.getcwd() + "\\Upload_Document.docx", self._upload_button, locatorType="xpath")
        sleep(5)
        self.elementCLick(self._text_submit, locatorType="xpath")

    def textInput(self, textData):
        self.waitForElement(self._text, locatorType="xpath")
        self.sendKeys(textData, self._text, locatorType="xpath")
        self.elementCLick(self._text_submit, locatorType="xpath")

    def hitEpic(self, epic, appName):
        if epic == "epic_ACD":
            epicHit = "access to " + appName
        elif epic == "epic_AE":
            epicHit = "issue with " + appName
        elif epic == "epic_X":
            epicHit = "reset password for " + appName
        else:
            epicHit = " "
            self.log.info("No such epic hit for this epic!!")

        self.log.info("Epic name is: " + epic + " and epic hit used is: " + epicHit)
        return epicHit


    def writeUserInput(self, userInput, epic, appName, actionType, scope, keyPhrase):
        if "Button_" in userInput:
            self.buttons(userInput)
        elif "AppName" in userInput:
            epicHit = self.hitEpic(epic, appName)
            self.textInput(epicHit)
        elif "FaultType" in userInput:
            faultType = appfile_read.getActionType(actionType)
            self.textInput(faultType)
        elif "MoreApp" in userInput:
            self.textInput(appName + " (" + scope + ")")
        elif "MoreFault" in userInput:
            self.textInput(actionType + " (" + keyPhrase + ")")
        elif "Upload" in userInput:
            self.upload()
        else:
            self.textInput("test")

    def questions_func(self, bubble, questions):
        if questions:
            bubble = re.sub('[\s|\W]', '', bubble)
            match = self.util.verifyTextMatch(bubble, questions[0])
            if match:
                result = 'Match'
                questions.pop(0)
            else:
                notOrder = self.util.verifyTextInList(bubble, questions)
                if notOrder:
                    result = 'NotOrder'
                    questions.pop(notOrder)
                else:
                    result = False

            return result

    def notes(self, bubble, notes):
        if notes:
            result = self.util.verifyTextMatch(bubble, notes)
            return result

    def link(self, bubble, link):
        if link:
            result = self.util.verifyTextContains(bubble, link)
            return result

    def saveChat(self, appName, actionType):
        self.savePage(appName, actionType)

    def getTicket(self, bubble, tobiLemma):
        regex_ticket = re.findall(r'\bREQ|[\d]', bubble)
        if regex_ticket != [] and tobiLemma == 'REQ_ID':
            ticket = "".join(map(str, regex_ticket))
            self.log.info("Ticket is created with ID: " + str(ticket))
            return ticket
        else:
            self.log.info("The bubble doesn't contain REQ")
            return False

    def saveResults(self, demandID, status, ticketID, Questions, Notes):
        excel_write_data.writeFileRows(demandID, status, ticketID, Questions, Notes)

    def chatFLow(self, keyPhrase, appName, actionType, scope, link, notes, q1, q2, q3, q4, q5, q6):

        #App file info:
        keyPhrase = appfile_read.getKeyPhrase(keyPhrase)
        epic = appfile_read.getEpic(keyPhrase)
        appName = appfile_read.getAppName(appName)
        actionType = appfile_read.getActionType(actionType)
        scope = appfile_read.getScope(scope)
        questions = appfile_read.getQuestions(q1, q2, q3, q4, q5, q6)
        notes = appfile_read.getNotes(notes)
        link = appfile_read.getUrl(link)
        questionsLen = appfile_read.getQuestionsLen(q1, q2, q3, q4, q5, q6)

        #Chat file info:
        chatFile = self.getChatFile(epic, link)
        chatFile_row = 1
        chatFile_col = 1
        chatOutput = self.readChatFile(chatFile, chatFile_row, chatFile_col)

        #Bubble info:
        bubbleCount = 1

        #Intializers
        result = False
        ticketID = 'No ticket created yet'
        demandID = str(appName + '_' + actionType)
        linkComment = 'No link for this app'
        notesComment = ''
        questionsComment = ''
        questionCount = 0
        notOrderCount = 0
        askedQuestions = []

        try:
            while chatOutput is not None:
                linkFlag = 0
                notesFlag = 0
                questionFlag = 0

                bubble = self.getBubble(bubbleCount)
                questions_output = self.questions_func(bubble, questions)
                if self.link(bubble, link):
                    bubbleCount = bubbleCount + 1
                    result = True
                    linkFlag = 1
                    linkComment = "The Link appeared in chat and passed"

                elif self.notes(bubble, notes):
                    bubbleCount = bubbleCount + 1
                    result = True
                    notesFlag = 1
                    notesComment = "The Notes appeared in chat and passed"

                elif questions_output:
                    bubbleCount = bubbleCount + 1
                    result = True
                    questionFlag = 1
                    questionCount = questionCount + 1
                    askedQuestions.append(bubble)
                    if questions_output is 'NotOrder':
                        notOrderCount = notOrderCount + 1

                else:
                    tobiLemma = chatOutput[0]
                    result = self.getTicket(bubble, tobiLemma)
                    if result:
                        ticketID = result

                    else:
                        result = self.compareChat(tobiLemma, bubble)
                        while (not result) and (chatOutput is not None):
                            chatFile_col = chatFile_col + 2
                            chatOutput = self.readChatFile(chatFile, chatFile_row, chatFile_col)
                            tobiLemma = chatOutput[0]
                            result = self.compareChat(tobiLemma, bubble)

                if result:
                    if questionFlag or notesFlag:
                        self.textInput("test")

                    else:
                        userInput = chatOutput[1]
                        if userInput is not None:
                            self.writeUserInput(userInput, epic, appName, actionType, scope, keyPhrase)
                            chatFile_row = chatFile_row + 1
                            bubbleCount = bubbleCount + 1
                            chatOutput = self.readChatFile(chatFile, chatFile_row, chatFile_col)

                        else:
                            chatFile_row = chatFile_row + 1
                            chatOutput = self.readChatFile(chatFile, chatFile_row, chatFile_col)
                            if not (questionFlag or notesFlag or linkFlag):
                                bubbleCount = bubbleCount + 1

                else:
                    self.log.error("Result is false")
                    print_stack()
                    break
        except:
            result = False
            self.saveChat(appName, actionType)
            print_stack()

        else:
            self.saveChat(appName, actionType)

        #Log comments

            if link:
                if linkComment:
                    self.log.info(linkComment)
                else:
                    self.log.error("CHECK Link: Link is not displayed in the chat!!!")
                    result = False
            if notes:
                if notesComment:
                    self.log.info(notesComment)
                else:
                    notesComment = "CHECK NOTES: Notes are not displayed in the chat!!!"
                    self.log.error(notesComment)
                    result = False
            if questionsLen:
                self.log.info("Expected number of questions is: " + str(questionsLen) + " and actual number of questions is: " + str(questionCount))
                if questionCount == questionsLen:
                    if notOrderCount:
                        questionsComment = 'CHECK!! questions are not ordered, but all questions are asked'
                        result = False
                    else:
                        questionsComment = 'All questions are asked in order'
                    self.log.info(questionsComment)
                else:
                    self.log.info("Asked questions are: " + str(askedQuestions))
                    if notOrderCount:
                        questionsComment = 'CHECK QUESTIONS: not all questions are asked!! and asked questions are not ordered'
                    else:
                        questionsComment = 'CHECK QUESTIONS: not all questions are asked!!'
                    self.log.error(questionsComment)
                    result = False

        self.log.info(
            "The chat file row count is: " + str(chatFile_row) + " and chat file column count is: " + str(chatFile_col))
        self.log.info("The chat bubble count is: " + str(bubbleCount))
        if result:
            status = 'Passed'
            self.saveResults(demandID, status, ticketID, questionsComment, notesComment)
        else:
            status = 'Failed'
            self.saveResults(demandID, status, ticketID, questionsComment, notesComment)
        return result