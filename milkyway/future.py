# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''

@author: Federico Ressi
'''

from collections import namedtuple
import logging
import sys
import threading
from traceback import format_exception


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_ExceptionInfo = namedtuple(
    'ExceptionInfo', ['exception', 'trace', 'thread_name'])
'''
Class used to store information of an exception
'''

_NO_RESULT = object()


class FutureCall(object):

    'Calls a function and stores its execution result.'

    # value returned by function
    _result = _NO_RESULT

    # ExceptionInfo with the exception raised by function
    _exception = None

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        try:
            self._result = self._func(*self._args, **self._kwargs)

        except Exception as exc:
            exc_type, _, exc_tb = sys.exc_info()
            self._exception = _ExceptionInfo(
                exception=exc,
                trace=format_exception(exc_type, exc, exc_tb),
                thread_name=threading.current_thread().name)
            self._unhandled_exception(exc_type, exc, exc_tb)

    @property
    def done(self):
        'Returns True when execution is complete.'
        result = self._result
        if result is _NO_RESULT:
            exception = self._exception
            if exception:
                return True

            else:
                return False

        else:
            return True

    @property
    def result(self):
        'Returns produced result or raises a FutureCallException'
        result = self._result
        if result is _NO_RESULT:
            exception = self._exception
            if exception:
                raise ConcurrentException(
                    cause=self._exception,
                    message='Exception raised in future call.')

            else:
                raise RuntimeError('Future call not executed.')
        else:
            return result

    @property
    def exception(self):
        'Return produced exception or None.'

        exception = self._exception
        if exception:
            return exception.exception

        else:
            result = self._result
            if result is _NO_RESULT:
                raise RuntimeError('Future call not executed.')

            else:
                return None

    @staticmethod
    def _unhandled_exception(exc_type, value, exc_tb):
        'Called when inner function raises an exception.'
        sys.excepthook(exc_type, value, exc_tb)


_CONCURRENT_EXCEPTION_MESSAGE_FORMAT = '''{}

Caused in thread {} by:
{}'''


class ConcurrentException(Exception):

    '''
    Exception raised by result method when an exception was raised during
    execution.
    '''

    def __init__(self, cause, message=''):
        super(ConcurrentException, self).__init__()
        self._cause = cause
        self._message = message

    def raise_cause(self):
        'Raises the exception raised during call execution.'
        raise self._cause.exception

    @property
    def cause(self):
        'Exception that caused this one.'
        return self._cause.exception

    def __str__(self):
        return _CONCURRENT_EXCEPTION_MESSAGE_FORMAT.format(
            self._message, self._cause.thread_name, ''.join(self._cause.trace))
