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


class View(object):

    '''
    Base class of all views
    '''

    __metaclass__ = ABCMeta

    def __init__(self, presenter=None, create_presenter=None):

        # initialize presenter and model
        if presenter is None:

            if create_presenter is None:
                # pylint: disable=assignment-from-no-return
                presenter = self._create_presenter()

            else:
                assert callable(create_presenter)
                presenter = create_presenter()

        assert isinstance(presenter, Presenter)
        self._presenter = presenter

        # initialize view
        self.initialize()

    def _create_presenter(self):
        '''
        Creates a presenter for this view when it is not given.
        '''

        raise ValueError('A presenter is required.')

    def initialize(self):
        '''
        Initialize view, presenter and model
        '''
        self._initialize_view()
        self._presenter.initialize()

    @abstractmethod
    def _initialize_view(self):
        '''
        Setup view widgets
        '''

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

    model_class = Model

    view_class = View

    def __init__(self, view, model=None):
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

        assert isinstance(view, self.view_class),\
            "{} is not an instance of {}".format(view, self.view_class)
        self._view = view

        if model is None:
            model = self._create_model()
        assert isinstance(model, self.model_class),\
            "{} is not an instance of {}".format(model, self.model_class)
        self._model = model

    def _create_model(self):
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
