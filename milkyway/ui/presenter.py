# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# Created:    Oct 11, 2014
# Modified:   __updated__
# -----------------------------------------------------------------------------

'''

@author: Federico Ressi
'''

from __future__ import division

import logging


logger = logging.getLogger(__name__)


class Presenter(object):

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

        self._view = view
        self._model = model
