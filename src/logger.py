""" logging utils """

import os
import logging
import logging.handlers as handlers

LOGGING_MSG_FORMAT  = '%(asctime)s %(levelname)s %(message)s'
LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_logger(name, filepath, with_pid=True):
    """ get logger """

    logger = logging.getLogger(name)
    if with_pid:
        logfilepath = "%s.%s" % (filepath, os.getpid())
    else:
        logfilepath = filepath

    hdlr = handlers.TimedRotatingFileHandler(logfilepath, when='MIDNIGHT')
    formatter = logging.Formatter(LOGGING_MSG_FORMAT)
    hdlr.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(hdlr)
    return logger

def close_logger(logger):
    """ close logger """

    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
