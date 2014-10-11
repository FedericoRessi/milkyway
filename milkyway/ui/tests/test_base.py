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

from milkyway.ui.base import Model, View, Presenter


@fixture
def view():
    '''
    Any view
    '''

    return Mock(spec=View)


@fixture
def model():
    '''
    Any model
    '''

    return Mock(spec=Model)


@fixture
def presenter():
    '''
    Any model
    '''

    return Mock(spec=Presenter)


class DummyPresenter(Presenter):

    '''
    Dummy presenter implementation
    '''

    def __init__(self, *args, **kwargs):
        self._create_model = Mock(spec=Model)
        super(DummyPresenter, self).__init__(*args, **kwargs)


def test_create_presenter_with_create_model(view):
    '''
    Test base presenter constructor with a view
    '''

    presenter = DummyPresenter(view=view)

    presenter._create_model.assert_called_once_with()
    assert presenter._view is view
    assert presenter._model is presenter._create_model()


def test_create_presenter_without_model(view):
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


class DummyView(View):

    '''
    Dummy class for testing class View
    '''

    _initialized = False
    _disposed = False

    def __init__(self, presenter=None, create_presenter=None):
        if create_presenter:
            self._create_presenter = create_presenter
        super(DummyView, self).__init__(presenter=presenter)

    def _initialize_view(self):
        assert not self._initialized
        self._initialized = True

    def _dispose_view(self):
        assert not self._disposed
        self._disposed = True


def test_create_view_with_presenter(presenter):
    view = DummyView(presenter=presenter)
    assert view._presenter is presenter
    view._presenter.initialize.assert_called_once_with()


def test_create_view_creating_presenter():
    create_presenter = Mock(return_value=Mock(spec=Presenter))
    view = DummyView(create_presenter=create_presenter)
    assert view._presenter is view._create_presenter()
    view._presenter.initialize.assert_called_once_with()


def test_create_view_without_presenter():
    with raises(ValueError):
        DummyView()
