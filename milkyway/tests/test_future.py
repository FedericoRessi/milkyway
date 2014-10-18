# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------

'''
Test milkyway.future package.

@author: Federico Ressi
'''

import threading

from pytest import fixture, raises

from milkyway.future import FutureCallException


@fixture
def future_call_exception():
    try:
        raise ValueError('inner error')

    except ValueError as cause:

        return FutureCallException(
            message='outer error', cause=cause,
            thread_name=threading.current_thread().name
            stack_trace=stack_trace)


def test_future_call_exception_raise_cause(future_call_exception):
    with raises(ValueError):
        future_call_exception.raise_cause()
