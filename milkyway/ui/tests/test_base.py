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
        self._create_model = Mock(spec=callable, return_value=Mock(spec=Model))
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

    presenter = Presenter(view=view)
    assert isinstance(presenter._model, presenter.model_class)
    assert presenter._view is view


def test_create_presenter_without_view():
    '''
    Test base presenter constructor without a view
    '''

    with raises(AssertionError):
        DummyPresenter(view=None)


def test_create_presenter_with_view_and_model(view, model):
    '''
    Test base presenter constructor with a view and a model
    '''

    presenter = Presenter(view=view, model=model)

    assert presenter._view is view
    assert presenter._model is model


def test_initialize_presenter(view, model):
    '''
    Test presenter disposer
    '''

    presenter = Presenter(view=view, model=model)
    presenter._initialize_presenter = Mock(spec=callable)

    presenter.initialize()

    presenter._initialize_presenter.assert_called_once_with()
    model.initialize.assert_called_once_with()


def test_dispose_presenter(view, model):
    '''
    Test presenter disposer
    '''

    presenter = Presenter(view=view, model=model)
    presenter._dispose_presenter = Mock(spec=callable)

    presenter.dispose()

    model.dispose.assert_called_once_with()
    presenter._dispose_presenter.assert_called_once_with()
    view.dispose.assert_called_once_with()
    assert not hasattr(presenter, '_model')
    assert not hasattr(presenter, '_view')


class DummyView(View):

    '''
    Dummy class for testing class View
    '''

    initialized = False
    disposed = False

    def _initialize_view(self):
        assert not self.initialized
        self.initialized = True

    def _dispose_view(self):
        assert not self.disposed
        self.disposed = True


def test_create_view_with_presenter(presenter):
    '''
    Test view creation with given presenter
    '''

    view = DummyView(presenter=presenter)
    assert view._presenter is presenter
    assert view.initialized
    view._presenter.initialize.assert_called_once_with()


def test_create_view_creating_presenter():
    '''
    Test view creation with create_present
    '''

    create_presenter = Mock(return_value=Mock(spec=Presenter))
    view = DummyView(create_presenter=create_presenter)
    assert view._presenter is create_presenter()
    assert view.initialized
    view._presenter.initialize.assert_called_once_with()


def test_create_view_without_presenter():
    '''
    Test view creation without present and present factory
    '''

    with raises(ValueError):
        DummyView()


def test_dispose_view(presenter):
    '''
    Test view disposition
    '''

    view = DummyView(presenter=presenter)

    view.dispose()

    assert view.disposed
    assert not hasattr(view, '_presenter')
