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

from milkyway.ui.main_window import MainWindowPresenter


@fixture
def view():
    '''
    Any view
    '''

    return Mock()


@fixture
def model():
    '''
    Any model
    '''

    return Mock()


def test_initialize(view, model):
    ''''Test '''

    presenter = MainWindowPresenter(view, model)
    presenter.initialize()

    assert model.current_view == model.MAIN_MENU
    view.show_main_menu.assert_called_once_with(
        enabled_options={model.NEW_GAME, model.QUIT})
