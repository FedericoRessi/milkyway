# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------

'''
Module for UI base classes

@author: Federico Ressi
'''

from abc import ABCMeta, abstractmethod
import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class View(object):

    '''
    Base class of all views
    '''

    __metaclass__ = ABCMeta

    def __init__(self, presenter=None):

        # initialize view
        self._initialize_view()

        # initialize presenter and model
        if presenter is None:
            presenter = self.create_presenter()
        self._presenter = presenter

        presenter.initialize()

    @abstractmethod
    def _initialize_view(self):
        '''
        Setup view widgets
        '''

    def create_presenter(self):
        '''
        Creates a presenter for this view when it is not given.
        '''

        raise ValueError('A presenter is required.')

    def dispose(self):
        '''Dispose this view.'''

        self._dispose_view()

        del self._presenter

    @abstractmethod
    def _dispose_view(self):
        '''
        Dispose view widgets
        '''


class Presenter(object):  # pylint: disable=too-few-public-methods

    '''
    Base class for all presenters
    '''

    __metaclass__ = ABCMeta

    def __init__(self, view, model=None):
        '''
        Base class for all presenters. A presenter must implements the
        behaviors of a view processing events and updating both model and view.

        :param view: the view the presenter is binded with
        :param model: the model for the presenter or None(optional)
        '''

        assert isinstance(view, View)

        if model is None:
            model = self.create_model()

        self._model = model
        self._view = view

    def create_model(self):
        '''
        Create a new model if not provided by the constructor.
        '''
        raise ValueError('Model is required.')

    def initialize(self):
        '''
        Initialize presenter and model
        '''
        self._initialize_presenter()
        self._model.initialize()

    def _initialize_presenter(self):
        '''
        Initialize initial model and view state
        '''

    def dispose(self):
        '''
        Dispose presenter, model and view
        '''
        self._dispose_presenter()
        self._view.dispose()
        self._model.dispose()
        del self._model
        del self._view

    def _dispose_presenter(self):
        '''
        Dispose presenter resources
        '''


class Model(object):

    '''
    Base class of all models
    '''

    __metaclass__ = ABCMeta

    def initialize(self):
        '''
        Initialize this model
        '''

    def dispose(self):
        '''
        Dispose this model
        '''


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
