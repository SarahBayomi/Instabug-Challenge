import inspect
import logging
from datetime import datetime

loggers = {}
def customLogger(logLevel=logging.DEBUG):
    global loggers
    # Gets the name of the class / method from where this method is called
    loggerName = inspect.stack()[1][3]
    if loggers.get(loggerName):
        return loggers.get(loggerName)
    else:
        logger = logging.getLogger(loggerName)
        # By default, log all messages
        logger.setLevel(logging.DEBUG)

        fileHandler = logging.FileHandler(datetime.now().strftime('logfile_%d_%m_%Y_%I_%M_%p.log'), mode='a')
        fileHandler.setLevel(logLevel)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.propagate = False
        loggers[loggerName] = logger

        return logger
