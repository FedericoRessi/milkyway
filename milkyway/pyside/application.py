# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
from sys import exc_info
from twisted.python.failure import _Traceback
'''

@author: Federico Ressi
'''

import logging
import sys
import threading
import traceback

from PySide.QtCore import QEvent, QObject
from PySide.QtGui import QApplication

from milkyway.future import FutureCall
from milkyway.pyside.main_window import MainWindow


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


_UNDEFINED_RESULT = object()


class _FutureCallEvent(FutureCall, QEvent):

    EVENT_TYPE = QEvent.Type(QEvent.registerEventType())


class _FutureCallEventHandler(QObject):

    def event(self, event):
        assert callable(event)
        event()
        return True


class Application(object):

    '''
    Milky Way application class
    '''

    _application = None
    _future_call_event_handler = None
    _main_window = None

    def __init__(self, argv=[]):
        logger.debug('Set up application.')
        self._application = QApplication(argv)
        self._future_call_event_handler = _FutureCallEvent()

        logger.debug('Set up main window.')
        self._main_window = MainWindow(application=self)

    def run(self):
        '''
        Show main window and execute and enter the event loop
        '''
        self._main_window.show()

        logger.debug('Enter event loop.')
        self._application.exec_()
        logger.debug('Event loop leaved.')

    def create_future_call(self, func, *args, **kwargs):
        return _FutureCallEvent(func, *args, **kwargs)

    def submit(self, func, *args, **kwargs):
        application = self._application
        if not application:
            raise RuntimeError('Application disposed.')

        future = self.create_future_call(func, *args, **kwargs)
        application.postEvent(self._future_call_event_handler, future)
        return future

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
            del self._future_call_event_handler
