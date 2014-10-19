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

from PySide.QtCore import QEvent, QObject
from PySide.QtGui import QApplication

from milkyway.future import FutureCall
from milkyway.pyside.main_window import MainWindow


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_UNDEFINED_RESULT = object()


class _FutureCallEvent(FutureCall, QEvent):

    'Event posted when a future call has to be executed on main thread.'

    _Q_EVENT_TYPE = QEvent.Type(QEvent.registerEventType())

    def __init__(self, func, *args, **kwargs):
        FutureCall.__init__(self, func, *args, **kwargs)
        QEvent.__init__(self, self._Q_EVENT_TYPE)


class _FutureCallHandler(  # pylint: disable=too-many-public-methods, no-init
        QObject):

    'Handler for executing future calls on main thread.'

    def event(self, event):
        assert callable(event)
        event()
        return True


class Application(object):

    '''
    Milky Way application class
    '''

    _application = None
    _future_call_handler = None
    _main_window = None

    @staticmethod
    def _init_qt_application(argv):
        'Initialize QT application if not done before'
        qt_application = QApplication.instance()
        if qt_application is None:
            logger.debug('Initialize QT application with arguments: %r', argv)
            qt_application = QApplication(argv)
        return qt_application

    def __init__(self, argv):
        logger.debug('Initialize application.')
        self._application = self._init_qt_application(argv=argv)
        self._future_call_handler = _FutureCallHandler()
        self._main_window = MainWindow()

    def run(self):
        '''
        Shows main window and enters the event loop
        '''
        self._main_window.show()

        logger.debug('Enter event loop.')
        self._application.exec_()
        logger.debug('Event loop leaved.')

    def submit(self, func, *args, **kwargs):
        'Submit a future call to be executed on main thread later.'
        application = self._application
        if not application:
            raise RuntimeError('Application disposed.')

        future_call = _FutureCallEvent(func, *args, **kwargs)
        application.postEvent(self._future_call_handler, future_call)
        return future_call

    def dispose(self):
        '''
        Dispose main window and application
        '''
        main_window = self._main_window
        if main_window:
            logger.debug('Dispose main window.')
            self._main_window.dispose()
            del self._main_window

        application = self._application
        if application:
            logger.debug('Dispose QApplication.')
            application.exit()
            del self._application
            del self._future_call_handler
