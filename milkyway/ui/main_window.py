# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''
Main window presenter and module


@author: Federico Ressi
'''

import logging

from milkyway.ui.presenter import Presenter


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MainWindowPresenter(Presenter):

    '''
    Presenter for the main game window
    '''

    def initialize(self):
        '''
        Called by my window to reach initial state
        '''

        self._model.current_view = self._model.MAIN_MENU
        self._view.show_main_menu(
            enabled_options={self._model.NEW_GAME, self._model.QUIT})
