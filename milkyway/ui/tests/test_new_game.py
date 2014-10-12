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

from milkyway.ui.new_game import NewGameModel, NewGameView, NewGamePresenter


@fixture
def model():
    '''
    Returns a mocked model
    '''
    return Mock(spec=NewGameModel)


@fixture
def view():
    '''
    Returns a mocked view
    '''
    return Mock(spec=NewGameView)


@fixture
def presenter():
    '''
    Returns a mocked presenter
    '''

    return Mock(spec=NewGamePresenter)


def test_initialize_presenter(model, view):
    '''
    Test new game presenter initialization
    '''

    presenter = NewGamePresenter(model=model, view=view)

    presenter.initialize()
    view.update.assert_called_once_with(
        enabled_options={NewGameModel.CANCEL},
        number_of_stars=model.number_of_stars)
