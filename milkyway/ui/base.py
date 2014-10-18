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


class View(object):  # pylint: disable=abstract-class-not-used

    '''
    Base class of all views
    '''

    __metaclass__ = ABCMeta

    def __init__(
            self, parent=None, presenter=None, create_presenter=None,
            name=None):

        if not name:
            name = type(self).__name__
        self._name = name

        assert parent is None or isinstance(parent, View)
        self._parent = parent

        # initialize presenter and model
        if presenter is None:
            logger.debug('%s: create presenter.', self._name)
            presenter = self._create_presenter(
                name=self._name, create_presenter=create_presenter)
        assert isinstance(presenter, Presenter)
        self._presenter = presenter

        # initialize view
        self.initialize()

    def _create_presenter(self, name, create_presenter):
        '''
        Creates a presenter for this view when it is not given.
        '''
        if not create_presenter:
            raise ValueError('A presenter is required.')

        assert callable(create_presenter)
        return create_presenter(name)

    def initialize(self):
        '''
        Initialize view, presenter and model
        '''
        logger.debug('%s: initialize view.', self._name)
        self._initialize_view()

        logger.debug('%s: initialize presenter.', self._name)
        self._presenter.initialize()

    @abstractmethod
    def _initialize_view(self):
        '''
        Setup view widgets
        '''

    def dispose(self):
        '''Dispose this view.'''

        logger.debug('%s: dispose view.', self._name)
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

    model_class = Model

    view_class = View

    def __init__(self, view, model=None, create_model=None, name=None):
        '''
        Base class for all presenters. A presenter must implements the
        behaviors of a view processing events and updating both model and view.

        :param view: the view the presenter is binded with
        :param model: the model for the presenter or None(optional)
        '''

        assert issubclass(self.view_class, View),\
            "{} is not a subclass of View".format(self.view_class)
        assert issubclass(self.model_class, Model),\
            "{} is not a subclass of Model".format(self.model_class)

        if name is None:
            name = type(self._name)
        self._name = name

        assert isinstance(view, self.view_class),\
            "{} is not an instance of {}".format(view, self.view_class)
        self._view = view

        if model is None:
            logger.debug('%s: create model.', name)
            model = self._create_model(name=name, create_model=create_model)
        assert isinstance(model, self.model_class),\
            "{} is not an instance of {}".format(model, self.model_class)
        self._model = model

    def _create_model(self, name, create_model):
        '''
        Creates a model of class model_class
        '''
        if create_model is None:
            
        return self.model_class()

    def initialize(self):
        '''
        Initialize presenter and model
        '''
        self._initialize_presenter()
        self._model.initialize()

    def _initialize_presenter(self):
        '''
        Initialize presenter resources
        '''

    def dispose(self):
        '''
        Dispose presenter, model and view
        '''
        self._model.dispose()
        self._dispose_presenter()
        self._view.dispose()
        del self._model
        del self._view

    def _dispose_presenter(self):
        '''
        Dispose presenter resources
        '''


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name
