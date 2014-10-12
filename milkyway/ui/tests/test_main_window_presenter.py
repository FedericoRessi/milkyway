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

from mock import Mock
from pytest import fixture  # pylint: disable=no-name-in-module

from milkyway.ui.main_window import MainWindowModel, MainWindowPresenter,\
    MainWindowView


@fixture
def view():
    '''
    Any view
    '''

    return Mock(spec=MainWindowView)


@fixture
def model():
    '''
    Any model
    '''

    return Mock(spec=MainWindowModel)


@fixture
def presenter():
    '''
    Any model
    '''

    return Mock(spec=MainWindowPresenter)


def test_initialize_presenter(view, model):
    ''''Test '''

    presenter = MainWindowPresenter(view, model)
    presenter.initialize()

    assert model.current_view == MainWindowModel.MAIN_MENU
    view.show_main_menu.assert_called_once_with(
        enabled_options={MainWindowModel.NEW_GAME, MainWindowModel.QUIT})


class DummyMainWindowView(MainWindowView):

    '''
    Dummy class for testing MainWindowView
    '''

    initialized = False

    disposed = False

    main_menu_enabled_options = None

    def _initialize_view(self):
        self.initialized = True

    def _dispose_view(self):
        self.disposed = True

    def show_main_menu(self, enabled_options):
        self.main_menu_enabled_options = enabled_options


def test_create_view_presenter():
    ''''Test presenter creation by MainWindowView'''

    view = DummyMainWindowView()
    presenter = view._create_presenter()
    assert isinstance(presenter, MainWindowPresenter)
    assert presenter._view is view
    assert isinstance(presenter._model, MainWindowModel)
