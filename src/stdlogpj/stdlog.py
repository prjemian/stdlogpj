#!/usr/bin/env python

"""
python logging done my way

* terse output to stream (console)
* extended output to log file in `.logs` subdirectory
* can save logs in a named directory

:see: https://docs.python.org/3/library/logging.html

similar projects:

* https://github.com/fx-kirin/py-stdlogging
* https://github.com/caproto/caproto/blob/master/caproto/_log.py
"""

import logging, logging.handlers
import os

LOG_DIR_BASE = ".logs"
DEFAULT_LOGGING_LEVEL = logging.DEBUG


__all__ = [
    "standard_logging_setup",
    "consoleReportHandler",
    "fileReportHandler"
]


class consoleReportHandler(logging.StreamHandler):
    """
    logging reports to the console should be brief

    EXAMPLE::

        logger.info(f"writing to SPEC file: {specwriter.spec_filename}")
    
    results in::

        I Fri-12:43:19 - writing to SPEC file: /tmp/20200214-124319.dat

    The first letter shows the (first letter of the) logging level.
    The date/time shows the weekday abbreivation and the 24-hour time.
    More details should be logged in a file with a different handler.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFormatter(
            logging.Formatter(
                (
                    # nice output format
                    # https://docs.python.org/3/library/logging.html#logrecord-attributes
                    "%(levelname)-.1s",		# only first letter
                    " %(asctime)s"
                    " - "
                    "%(message)s"
                ),
                datefmt="%a-%H:%M:%S"))     # weekday & 24h time of day
        self.formatter.default_msec_format = "%s.%03d"


def fileReportHandler(
        logger_name,
        file_name_base=None,
        maxBytes=0,
        backupCount=0,
        log_path=None,
):
    """
    log reports to a file should be verbose to aid problem diagnosis

    See ``standard_logging_setup()`` for parameter documentation.

    EXAMPLE::

        logger.info(f"writing to SPEC file: {specwriter.spec_filename}")
    
    results in::

        |2020-02-14 12:43:19.180|INFO|12056|bluesky-session|callbacks|29|MainThread| - writing to SPEC file: /tmp/20200214-124319.dat

    The metadata is distinct from the message.
    The separator between metadata items is a vertical bar(``|``).
    The metadata items are: asctime, levelname, PID, name, module, lineno, & threadName
    A full date/time stamp is reported per ISO-8601.  
    The reported time precision is limited to milliseconds.
    The process identifier helps to identify which bluesky session
    (such as restarts of the console).
    The module name and line number localize the log message to specific code.
    The thread name is reported as an additional diagnostic.
    """

    file_name_base = file_name_base or logger_name

    log_path = log_path or os.path.join(os.getcwd(), LOG_DIR_BASE)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_file = os.path.join(log_path, f"{file_name_base}.log")

    if maxBytes > 0 or backupCount > 0:
        handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=maxBytes, backupCount=backupCount)
    else:
        handler = logging.FileHandler(log_file)
    handler.setFormatter(
        logging.Formatter(
            (
                "|%(asctime)s"
                "|%(levelname)s"
                "|%(process)d"
                "|%(name)s"
                "|%(module)s"
                "|%(lineno)d"
                "|%(threadName)s"
                "| - "
                "%(message)s"
            )
        ))
    handler.formatter.default_msec_format = "%s.%03d"

    return handler


def standard_logging_setup(logger_name, 
                           file_name_base=None,
                           maxBytes=0,
                           backupCount=0,
                           log_path=None,
                           level=None,
                           ):
    """
    standard setup for logging
        
    PARAMETERS
    
    logger_name : str
        name of the the logger
    
    file_name_base : str
        Part of the name to store the log file.
        Full name is `f"<log_path>/{file_name_base}.log"`
        in present working directory.
    
    log_path : str
        Part of the name to store the log file.
        Full name is `f"<log_path>/{file_name_base}.log"`
        in present working directory.

        default: (the present working directory)/LOG_DIR_BASE
    
    level : int
        Threshold for reporting messages with this logger.
        Logging messages which are less severe than *level* will be ignored.

        default: 10 (``logging.DEBUG``), set by ``DEFAULT_LOGGING_LEVEL``

        see: https://docs.python.org/3/library/logging.html#levels
    
    maxBytes : (optional) int
        Log file *rollover* begins whenever the current 
        log file is nearly *maxBytes* in length.

        default: 0
    
    backupCount : (optional) int
        When *backupCount* is non-zero, the system will keep
        up to *backupCount* numbered log files (with added extensions
        `.1`, '.2`, ...).  The current log file always has no
        numbered extension.  The previous log file is the 
        one with the lowest extension number.

        default: 0
    
    **Note**:  When either *maxBytes* or *backupCount* are zero,
    log file rollover never occurs, so you generally want to set 
    *backupCount* to at least 1, and have a non-zero *maxBytes*.
    """

    level = level or DEFAULT_LOGGING_LEVEL
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    logger.addHandler(consoleReportHandler())
    logger.addHandler(
        fileReportHandler(
            logger_name,
            file_name_base=file_name_base,
            maxBytes=maxBytes,
            backupCount=backupCount,
            log_path=log_path,
        )
    )

    return logger
