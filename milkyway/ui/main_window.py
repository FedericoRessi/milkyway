# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''
Main window presente, module and view


@author: Federico Ressi
'''

from abc import ABCMeta, abstractmethod
import logging

from milkyway.ui.base import View, Presenter, Model


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MainWindowPresenter(Presenter):

    '''
    Presenter for the main game window
    '''

    def create_model(self):
        return MainWindowModel()

    def initialize(self):
        '''
        Called by my window to reach initial state
        '''

        assert isinstance(self._view, MainWindowView)

        self._model.current_view = self._model.MAIN_MENU
        self._view.show_main_menu(
            enabled_options={self._model.NEW_GAME, self._model.QUIT})


class MainWindowModel(Model):

    '''
    Main window model
    '''

    QUIT = 0
    MAIN_MENU = 1
    NEW_GAME = 2

    current_view = MAIN_MENU


class MainWindowView(View):

    '''
    Main window view
    '''

    __metaclass__ = ABCMeta

    def create_presenter(self):
        return MainWindowPresenter(self)

    @abstractmethod
    def show_main_menu(self, enabled_options):
        '''
        Show main menu
        '''
