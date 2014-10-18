# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------


'''

@author: Federico Ressi
'''

import logging
import sys
import threading
import traceback


logger = logging.getLogger(__name__)


class FutureCallException(Exception):

    def __init__(self, message, cause, thread_name, stack_trace):
        super(FutureCallException).__init__(message)
        self.message = message
        self.cause = cause
        self.thread_name = thread_name
        self.stack_trace = stack_trace

    def raise_cause(self):
        raise self.cause

    def __str__(self):
        return "{} raised in thread '{}' by {}".format(
            self.message, self.thread_name, self.stack_trace)


_UMPRODUCED_RESULT = object()


class FutureCall(object):

    _result = _UMPRODUCED_RESULT
    _exception = None

    def __init__(self, func, *args, **kwargs):
        super(FutureCall, self).__init__()
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        try:
            self._result = self.func(*self._args, **self._kwargs)

        except Exception as cause:
            exc_info = sys.exc_info()
            thread_name = threading.current_thread().name
            stack_trace = traceback.format_exception(*exc_info)
            message = 'Exception raised inside future call'
            self._exception = FutureCallException(
                message, cause, thread_name, stack_trace)

            logger.debug(message, exc_info=exc_info)
            self._unhandled_exception(exc_info)

    @property
    def done(self):
        result = self._result
        if result is _UMPRODUCED_RESULT:
            exception = self._exception
            if exception:
                return True

            else:
                return False

        else:
            return True

    @property
    def result(self):
        result = self._result
        if result is _UMPRODUCED_RESULT:
            exception = self._exception
            if exception:
                raise exception

            else:
                raise RuntimeError('Future call not executed.')
        else:
            return result

    @property
    def exception(self):
        exception = self._exception
        if exception:
            return exception.cause

        else:
            result = self._result
            if result is _UMPRODUCED_RESULT:
                raise RuntimeError('Future call not executed.')

            else:
                return None
