from pages.login.login_page import LoginPage
from pages.chat.chat_page import ChatPage
from pages import appfile_read
import unittest
import pytest
from utilities.teststatus import TestStatus
from utilities.read_data import getCSVData
from ddt import ddt, data, unpack
from pathlib import Path

@pytest.mark.usefixtures("oneTimeSetUp", "setUp")
@ddt
class DemandTests(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def objectSetup(self, setUp):
        self.lp = LoginPage(self.driver)
        self.chat = ChatPage(self.driver)
        self.ts = TestStatus(self.driver)

    @data(*getCSVData(Path(__package__).parent / "appfile.csv"))
    @unpack
    def test_validLogin(self, scope, keyPhrase, appName, actionType, link, notes, q1, q2, q3, q4, q5, q6):
        email = appfile_read.getScopeEmail(scope)
        password = appfile_read.getPassword()
        self.lp.login(email, password)
        result = self.lp.verifyLoginSuccessful()
        if result:
            result = self.chat.chatFLow(keyPhrase, appName, actionType, scope, link, notes, q1, q2, q3, q4, q5, q6)
            self.ts.markFinal('Testcase Failed', result, "Failed")
        else:
            self.ts.markFinal('Testcase Failed', result, "Failed Login")
