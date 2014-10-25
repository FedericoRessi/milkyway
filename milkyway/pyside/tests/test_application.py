# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# pylint: disable=protected-access,redefined-outer-name,invalid-name
# -----------------------------------------------------------------------------
'''
Test module for milkyway package.

@author: Federico Ressi
'''

from mock import patch
from pytest import mark  # pylint: disable=no-name-in-module

from PySide.QtGui import QApplication

from milkyway.future import FutureCall
from milkyway.pyside.application import Application


@patch('milkyway.pyside.application.QApplication')
def test_init_qt_application_when_not_instanced(qapplication_class):
    'Test constructor passes arguments to QT and creates main window'

    qapplication_class.instance.return_value = None

    application = Application._init_qt_application(['a', 'b'])
    assert application is qapplication_class.return_value
    qapplication_class.instance.assert_called_once_with()
    qapplication_class.assert_called_once_with(['a', 'b'])


@patch('milkyway.pyside.application.QApplication')
def test_init_qt_application_when_instanced(qapplication_class):
    'Test constructor passes arguments to QT and creates main window'

    application = Application._init_qt_application(['a', 'b'])
    assert application is qapplication_class.instance.return_value
    qapplication_class.instance.assert_called_once_with()
    assert not qapplication_class.called


@patch('milkyway.pyside.application.MainWindow')
@patch('milkyway.pyside.application.Application._init_qt_application')
def test_application_constructor(init_qt_application, main_window_class):
    'Test constructor passes arguments to QT and creates main window'

    application = Application(['a', 'b'])

    main_window_class.assert_called_once_with()
    init_qt_application.assert_called_once_with(argv=['a', 'b'])
    del application


@patch('milkyway.pyside.application.MainWindow')
@patch('milkyway.pyside.application.Application._init_qt_application')
def test_application_run(init_qt_application, main_window_class):
    'Test run method shows main window and enters event loop.'
    application = Application(['a', 'b'])

    application.run()

    main_window_class().show.assert_called_once_with()
    init_qt_application().exec_.assert_called_once_with()


@mark.crash
def test_submit_successeful_callback():
    'Test delayed execution of successful call-backs'

    application = Application(['a', 'b'])

    def add(a, b):
        'Dummy function that add two elements.'
        return a + b

    future = application.submit(add, 3, 5)
    assert isinstance(future, FutureCall)
    assert not future.done

    QApplication.processEvents(maxtime=5000)
    assert future.done
    assert 8 == future.result


@mark.crash
def test_submit_failing_callback():
    'Test delayed execution of successful call-backs'

    application = Application(['a', 'b'])

    def add(a, b):
        'Dummy function that add two elements.'
        return a + b

    future = application.submit(add, 3, 'CINQUE')
    assert isinstance(future, FutureCall)
    assert not future.done

    QApplication.processEvents(maxtime=5000)
    assert future.done
    assert isinstance(future.exception, TypeError)
