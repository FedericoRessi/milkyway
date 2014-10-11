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


class DummyPresenter(Presenter):

    '''
    Dummy presenter implementation
    '''

    def __init__(self, *args, **kwargs):
        self.create_model = Mock()
        super(DummyPresenter, self).__init__(*args, **kwargs)


def test_constructor_with_create_model(view):
    '''
    Test base presenter constructor with a view
    '''

    presenter = DummyPresenter(view=view)

    presenter.create_model.assert_called_once_with()
    assert presenter._view is view
    assert presenter._model is presenter.create_model()


def test_constructor_without_model(view):
    '''
    Test base presenter constructor with a view
    '''

    with raises(ValueError):
        Presenter(view=view)


def test_constructor_without_view():
    '''
    Test base presenter constructor without a view
    '''

    with raises(AssertionError):
        DummyPresenter(view=None)


def test_constructor_with_view_and_model(view, model):
    '''
    Test base presenter constructor with a view and a model
    '''

    presenter = Presenter(view=view, model=model)

    assert presenter._view is view
    assert presenter._model is model
