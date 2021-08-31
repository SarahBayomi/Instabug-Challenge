import utilities.custom_logger as cl
from utilities.util import Util
import logging
import re

log = cl.customLogger(logging.DEBUG)

def getScope(scope):
    scope = scope.strip()
    scope = scope.lower()
    return scope

def getScopeEmail(scope):
    scope = getScope(scope)
    if scope == "uk fixed line":
        email = "uk.viewer@vodafone.com"
    elif scope == "uk mobile":
        email = "UKtest.User2@vodafone.com"
    elif scope == "vssr":
        email = "testuser.vssr1@vodafone.com"
    elif scope == "vssb":
        email = "testuser.vssb@vodafone.com"
    elif scope == "vssi":
        email = "VISPLTEST.User@vodafone.com"
    else:
        email = " "
        log.info("No email found for this scope!!")

    log.info("Email used: " + email + " for scope: " + scope)
    return email

def getPassword():
    password = "Tobi@CT01"
    return password

def getKeyPhrase(keyPhrase):
    keyPhrase = keyPhrase.strip()
    keyPhrase = keyPhrase.lower()
    return keyPhrase

def getEpic(keyPhrase):
    keyPhrase = getKeyPhrase(keyPhrase)
    if "service request" in keyPhrase:
        epic = "epic_ACD"

    elif "application access" in keyPhrase:
        epic = "epic_ACD"

    elif "incident" in keyPhrase:
        epic = "epic_AE"

    elif "password reset" in keyPhrase:
        epic = "epic_X"

    else:
        epic = " "
        log.info("No Epic found for this key phrase!!")

    log.info("Epic is: " + epic + " for key phrase: " + keyPhrase)
    return epic

def getActionType(actionType):
    actionType = actionType
    log.info("Action Type is: " + actionType)
    return actionType

def getAppName(appName):
    appName = appName
    log.info("Application name is: " + appName)
    return appName

def getUrl(url):
    if url != '':
        url = url
        url = Util().cleanseURL(url)
        log.info("Link for this application is: " + url)
        return url
    else:
        log.info("No Link for this application!!")
        return False

def getNotes(notes):
    if notes != '':
        notes = notes.strip()
        notes = notes.lower()
        notes = re.sub('[\s|\W]', '', notes)
        log.info("Notes for this application is: " + notes)
        return notes
    else:
        log.info("No notes for this application!!")
        return False

def getQuestionsLen(q1, q2, q3, q4, q5, q6):
    if q1 == '':
        log.info("No questions for this application!!")
        return False
    else:
        if q2 == '':
            return 1
        else:
            if q3 == '':
                return 2
            else:
                if q4 == '':
                    return 3
                else:
                    if q5 == '':
                        return 4
                    else:
                        if q6 == '':
                            return 5
                        else:
                            return 6

def getQuestions(q1, q2, q3, q4, q5, q6):
    if q1 == '':
        log.info("No questions for this application!!")
        return False
    else:
        if q2 == '':
            log.info("Only 1 question for this application!!")
            log.info("Question 1 is: " + q1)
            q1 = re.sub('[\s|\W]', '', q1)
            return [q1]
        else:
            if q3 == '':
                log.info("Only 2 questions for this application!!")
                log.info("Question 1 is: " + q1)
                log.info("Question 2 is: " + q2)
                q1 = re.sub('[\s|\W]', '', q1)
                q2 = re.sub('[\s|\W]', '', q2)
                return [q1, q2]
            else:
                if q4 == '':
                    log.info("Only 3 questions for this application!!")
                    log.info("Question 1 is: " + q1)
                    log.info("Question 2 is: " + q2)
                    log.info("Question 3 is: " + q3)
                    q1 = re.sub('[\s|\W]', '', q1)
                    q2 = re.sub('[\s|\W]', '', q2)
                    q3 = re.sub('[\s|\W]', '', q3)
                    return [q1, q2, q3]
                else:
                    if q5 == '':
                        log.info("Only 4 questions for this application!!")
                        log.info("Question 1 is: " + q1)
                        log.info("Question 2 is: " + q2)
                        log.info("Question 3 is: " + q3)
                        log.info("Question 4 is: " + q4)
                        q1 = re.sub('[\s|\W]', '', q1)
                        q2 = re.sub('[\s|\W]', '', q2)
                        q3 = re.sub('[\s|\W]', '', q3)
                        q4 = re.sub('[\s|\W]', '', q4)
                        return [q1, q2, q3, q4]
                    else:
                        if q6 == '':
                            log.info("Only 5 questions for this application!!")
                            log.info("Question 1 is: " + q1)
                            log.info("Question 2 is: " + q2)
                            log.info("Question 3 is: " + q3)
                            log.info("Question 4 is: " + q4)
                            log.info("Question 5 is: " + q5)
                            q1 = re.sub('[\s|\W]', '', q1)
                            q2 = re.sub('[\s|\W]', '', q2)
                            q3 = re.sub('[\s|\W]', '', q3)
                            q4 = re.sub('[\s|\W]', '', q4)
                            q5 = re.sub('[\s|\W]', '', q5)
                            return [q1, q2, q3, q4, q5]
                        else:
                            log.info("This application has 6 questions!!")
                            log.info("Question 1 is: " + q1)
                            log.info("Question 2 is: " + q2)
                            log.info("Question 3 is: " + q3)
                            log.info("Question 4 is: " + q4)
                            log.info("Question 5 is: " + q5)
                            log.info("Question 6 is: " + q6)
                            q1 = re.sub('[\s|\W]', '', q1)
                            q2 = re.sub('[\s|\W]', '', q2)
                            q3 = re.sub('[\s|\W]', '', q3)
                            q4 = re.sub('[\s|\W]', '', q4)
                            q5 = re.sub('[\s|\W]', '', q5)
                            q6 = re.sub('[\s|\W]', '', q6)
                            return [q1, q2, q3, q4, q5, q6]
