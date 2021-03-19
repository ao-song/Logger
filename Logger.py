#!/usr/bin/env python3

from abc import ABC
import logging
import logging.handlers
import syslog

class Logger(ABC):
    def __init__(self, appname, loglevel) -> None:
        self._formatter = logging.Formatter(
            '%(asctime)s %(name)s <%(levelname)s>: %(message)s')
        self._logger = logging.getLogger(appname)
        self._logger.setLevel(loglevel)
        super().__init__()

    def get_logger(self):
        return self._logger

class FileLogger(Logger):
    def __init__(self, appname, filename, loglevel=logging.DEBUG) -> None:
        super().__init__(appname, loglevel)
        handler = logging.FileHandler(filename)
        handler.setFormatter(self._formatter)
        self._logger.addHandler(handler)

class StdoutLogger(Logger):
    def __init__(self, appname, loglevel=logging.DEBUG) -> None:
        super().__init__(appname, loglevel)
        handler = logging.StreamHandler()
        handler.setFormatter(self._formatter)
        self._logger.addHandler(handler)

class SyslogLogger(Logger):
    def __init__(self, appname, address='/dev/log',
                 facility=syslog.LOG_USER, loglevel=logging.DEBUG) -> None:
        super().__init__(appname, loglevel)
        handler = logging.handlers.SysLogHandler(address, facility)
        self._formatter = logging.Formatter(
            '%(name)s <%(levelname)s>: %(message)s')
        handler.setFormatter(self._formatter)
        self._logger.addHandler(handler)

if __name__ == "__main__":
    print('TEST BEGIN')

    stdlog = StdoutLogger('stdout-test-app').get_logger()
    stdlog.debug('hello, this is stdout debug message')
    stdlog.info('hello, this is stdout info message')

    filelog = FileLogger('file-test-app', './tmp.log').get_logger()
    filelog.debug('hello, this is file debug message')
    filelog.info('hello, this is file info message')

    sysloglog = SyslogLogger('syslog-test-app').get_logger()
    sysloglog.debug('hello, this is sys debug message')
    sysloglog.info('hello, this is sys info message')

    print('TEST END')
