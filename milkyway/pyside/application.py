# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''

@author: Federico Ressi
'''

from PySide.QtGui import QApplication
import logging

from milkyway.pyside.main_window import MainWindow


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Application(object):

    '''
    Milky Way application class
    '''

    _applicaiton = None
    _main_window = None

    def __init__(self, argv):
        self._applicaiton = QApplication(argv)
        self._main_window = window = MainWindow()
        window.show()

    def run(self):
        '''
        Execute the application entering the event loop
        '''
        self._applicaiton.exec_()

    def dispose(self):
        '''
        Dispose main window and application
        '''

        self._main_window.dispose()
        del self._main_window
        del self._applicaiton
