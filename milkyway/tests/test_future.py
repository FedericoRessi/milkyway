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
from traceback import format_exception
import sys

from mock import Mock, ANY, patch
from pytest import fail, fixture, raises  # pylint: disable=no-name-in-module

from milkyway.future import ConcurrentException, _ExceptionInfo, FutureCall


def test_future_call_before_execution():
    'Test future call before execution'

    func = Mock()
    call = FutureCall(func, 10, second=5)

    assert not func.called
    assert not call.done

    with raises(RuntimeError):
        call.result  # pylint: disable=pointless-statement

    with raises(RuntimeError):
        call.exception  # pylint: disable=pointless-statement


def test_future_call_on_successeful_erecution():
    'Test future call after a successful execution'

    func = Mock(return_value=2)
    call = FutureCall(func, 10, second=5)

    result = call()

    assert result is None
    func.assert_called_once_with(10, second=5)
    assert call.done
    assert call.result == 2
    assert call.exception is None


@patch('milkyway.future.sys.excepthook')
def test_future_call_on_failing_execution(excepthook):
    'Test future call after failing execution'

    inner_exception = ZeroDivisionError('division by zero.')

    def failing_function(first, second):  # pylint: disable=unused-argument
        'Simple function raising inner exception'
        raise inner_exception

    func = Mock(spec=failing_function, side_effect=failing_function)
    call = FutureCall(func, first=1, second=0)

    result = call()

    assert result is None
    func.assert_called_once_with(first=1, second=0)
    assert call.done

    try:
        call.result

    except ConcurrentException as outer_exception:
        assert outer_exception.cause is inner_exception
        assert outer_exception.message == ''

    except Exception as exception:
        exception_type = type(exception).__name__
        fail('Expected ConcurrentException, but ' + exception_type + 'raised')

    else:
        fail('ConcurrentException not raised.')

    assert call.exception is inner_exception
    excepthook.assert_called_once_with(ZeroDivisionError, inner_exception, ANY)


@fixture
def exception_info():
    'ExceptionInfo used to create ConcurrentException instances.'
    try:
        raise ValueError('inner error')

    except ValueError as exceotion:
        exc_info = sys.exc_info()
        return _ExceptionInfo(
            exception=exceotion, trace=format_exception(*exc_info),
            thread_name=threading.current_thread().name)


def test_concurrent_exception_raise_cause(exception_info):
    'Test FutureCallException.raise-cause'

    exception = ConcurrentException(
        cause=exception_info, message='outer error')

    with raises(ValueError):
        exception.raise_cause()


def test_concurrent_exception_str(exception_info):
    'Test FutureCallException.raise-cause'
    exception = ConcurrentException(
        cause=exception_info, message='outer error')

    result = str(exception)

    assert 'outer error' in result
    assert 'Caused in thread MainThread by:' in result
    assert "raise ValueError(\'inner error\')" in result


def test_concurrent_exception_stack_trace(exception_info):
    'Test FutureCallException.raise-cause'
    try:
        raise ConcurrentException(cause=exception_info, message='outer error')

    except ConcurrentException:
        exc_info = sys.exc_info()
        result = ''.join(format_exception(*exc_info))

    assert 'raise ConcurrentException(cause=exception_info' in result
    assert 'outer error' in result
    assert 'Caused in thread MainThread by:' in result
    assert "raise ValueError(\'inner error\')" in result
