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

from milkyway.ui.presenter import Presenter


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


def test_constructor_with_view(view):
    '''
    Test base presenter constructor with a view
    '''

    presenter = Presenter(view=view)

    assert presenter._view is view
    assert presenter._model is None


def test_constructor_with_view_and_model(view, model):
    '''
    Test base presenter constructor with a view and a model
    '''

    presenter = Presenter(view=view, model=model)

    assert presenter._view is view
    assert presenter._model is model


def test_constructor_without_view():
    '''
    Test base presenter constructor without a view
    '''

    with raises(AssertionError):
        Presenter(view=None)
