# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------

'''

@author: Federico Ressi
'''

import logging


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Presenter(object):  # pylint: disable=too-few-public-methods

    '''
    Base class for all presenters
    '''

    def __init__(self, view, model=None):
        '''
        Base class for all presenters. A presenter must implements the
        behaviors of a view processing events and updating both model and view.

        :param view: the view the presenter is binded with
        :param model: the model for the presenter (optional)
        '''

        assert view is not None

        if model is None:
            model = self.create_model()

        self._model = model
        self._view = view

    def create_model(self):
        '''
        Create a new model if not provided by the constructor.
        '''
        raise ValueError('Model is required.')
