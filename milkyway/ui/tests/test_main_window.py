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
from pytest import fixture, raises  # pylint: disable=no-name-in-module

from milkyway.ui.main_window import MainWindowModel, MainWindowPresenter,\
    MainWindowView
from milkyway.ui.tests.test_base import DummyView


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

    assert model.current_view == MainWindowView.MAIN_MENU
    view.show_main_menu.assert_called_once_with(
        enabled_options={MainWindowView.NEW_GAME, MainWindowView.QUIT})


def test_quit_clicked(view, model):
    '''
    Test behavior when quit button is clicked
    '''

    presenter = MainWindowPresenter(view, model)

    presenter.quit_clicked()
    assert not hasattr(presenter, '_view')
    assert not hasattr(presenter, '_model')
    view.dispose.assert_called_once_with()
    model.dispose.assert_called_once_with()


def test_continue_game_clicked(view, model):
    '''
    Test behavior when continue game button is clicked
    '''

    presenter = MainWindowPresenter(view, model)
    with raises(NotImplementedError):
        presenter.continue_game_clicked()


def test_new_game_clicked(view, model):
    '''
    Test behavior when new game button is clicked
    '''

    presenter = MainWindowPresenter(view, model)

    presenter.new_game_clicked()

    assert model.current_view == MainWindowView.NEW_GAME
    view.show_new_game.assert_called_once_with()


def test_load_game_clicked(view, model):
    '''
    Test behavior when load game button is clicked
    '''

    presenter = MainWindowPresenter(view, model)
    with raises(NotImplementedError):
        presenter.load_game_clicked()


def test_save_game_clicked(view, model):
    '''
    Test behavior when save game button is clicked
    '''

    presenter = MainWindowPresenter(view, model)
    with raises(NotImplementedError):
        presenter.save_game_clicked()


def test_cancel_clicked(view, model):
    '''
    Test behavior when cancel panel button is clicked
    '''

    presenter = MainWindowPresenter(view, model)

    presenter.cancel_clicked()

    assert model.current_view == MainWindowView.MAIN_MENU
    view.show_main_menu.assert_called_once_with(
        enabled_options={MainWindowView.NEW_GAME, MainWindowView.QUIT})


def test_accepted_clicked(view, model):
    '''
    Test behavior when accept panel button is clicked
    '''
    presenter = MainWindowPresenter(view, model)
    with raises(NotImplementedError):
        presenter.accept_clicked()


class DummyMainWindowView(DummyView, MainWindowView):

    '''
    Dummy class for testing MainWindowView
    '''

    initialized = False

    disposed = False

    main_menu_enabled_options = None

    def show_main_menu(self, enabled_options):
        self.main_menu_enabled_options = enabled_options

    def show_new_game(self):
        pass


def test_create_view_presenter():
    '''Test presenter creation by MainWindowView'''

    view = DummyMainWindowView()
    presenter = view._create_presenter()
    assert isinstance(presenter, MainWindowPresenter)
    assert presenter._view is view
    assert isinstance(presenter._model, MainWindowModel)
