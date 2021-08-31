import pytest
from base.webdriverfactory import WebDriverFactory
import utilities.custom_logger as cl
import logging
from utilities import excel_write_data
from utilities.util import Util

log = cl.customLogger(logging.DEBUG)

@pytest.mark.hookwrapper
@pytest.fixture()
def setUp(request, browser, env):
    print("Running method level setUp")
    if env == "Stage":
        URL = "https://vodafone-amelia-stage-v3.ipsoft.com/Amelia/ui/VodafoneSD/chat?as=internal#ds"
        log.info("Environment used: " + env)
    elif env == "Uat":
        URL = "https://vodafone-amelia-uat-v3.ipsoft.com/Amelia/chat"
        log.info("Environment used: " + env)
    elif env == "Prod":
        URL = "https://tobi.vodafone.com"
        log.info("Environment used: " + env)
    else:
        URL= ''
        log.info("Please enter valid environment in the command line ex: --env Uat")

    wdf = WebDriverFactory(browser)
    driver = wdf.getWebDriverInstance(URL)

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    driver.quit()
    print("Running method level tearDown")

@pytest.fixture(scope="class")
def oneTimeSetUp():
    print("Running one time setUp")
    fileName = Util().create_dateFileName('%d_%m_%Y_%I_%M_%p', '_tickets.xlsx')
    sheetName = 'Tickets'
    fileDirectory = Util().createDirectory(fileName, '../tickets/')
    excel_write_data.createFile(fileDirectory, fileName, sheetName)
    yield
    print("Running one time tearDown")

def pytest_addoption(parser):
    parser.addoption("--browser")
    parser.addoption("--env")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")