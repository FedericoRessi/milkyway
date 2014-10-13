# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# pylint: disable=maybe-no-member,abstract-class-not-used
# -----------------------------------------------------------------------------
'''
Main window presente, module and view


@author: Federico Ressi
'''

from abc import ABCMeta, abstractmethod
import logging

from milkyway.ui.base import View, Presenter, Model


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MainWindowModel(Model):

    '''
    Main window model
    '''

    current_view = None


class MainWindowView(View):

    '''
    Main window view
    '''

    MAIN_MENU = 0
    CONTINUE_GAME = 1
    NEW_GAME = 2
    LOAD_GAME = 3
    SAVE_GAME = 4
    QUIT = 5

    __metaclass__ = ABCMeta

    def _create_presenter(self):
        return MainWindowPresenter(self)

    @abstractmethod
    def show_main_menu(self, enabled_options):
        '''
        Show main menu
        '''

    @abstractmethod
    def show_new_game(self):
        '''
        Show main menu
        '''


class MainWindowPresenter(Presenter):

    '''
    Presenter for the main game window
    '''

    model_class = MainWindowModel

    view_class = MainWindowView

    current_presenter = None

    def _initialize_presenter(self):
        '''
        Called by my window to reach initial state
        '''

        self._model.current_view = MainWindowView.MAIN_MENU
        self._view.show_main_menu(
            enabled_options={MainWindowView.NEW_GAME, MainWindowView.QUIT})

    def continue_game_clicked(self):
        '''
        Continue game button clicked
        '''
        raise NotImplementedError

    def new_game_clicked(self):
        '''
        New game button clicked
        '''
        self._model.current_view = MainWindowView.NEW_GAME
        self._view.show_new_game()

    def load_game_clicked(self):
        '''
        Load game button clicked
        '''
        raise NotImplementedError

    def save_game_clicked(self):
        '''
        Save game button clicked
        '''
        raise NotImplementedError

    def quit_clicked(self):
        '''
        Quit button clicked
        '''

        self.dispose()

    def cancel_clicked(self):
        '''
        Cancel panel button clicked
        '''
        self._model.current_view = MainWindowView.MAIN_MENU
        self._view.show_main_menu(
            enabled_options={MainWindowView.NEW_GAME, MainWindowView.QUIT})

    def accept_clicked(self):
        '''
        Accept panel button clicked
        '''
        raise NotImplementedError
