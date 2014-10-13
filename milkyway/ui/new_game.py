# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# pylint: disable=maybe-no-member,abstract-class-not-used
# -----------------------------------------------------------------------------
'''

@author: Federico Ressi
'''

from abc import abstractmethod
import logging

from milkyway.ui.base import Presenter, View, Model


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class NewGameModel(Model):

    '''
    Model class for new game panel
    '''

    number_of_stars = 100


class NewGameView(View):

    '''
    View interface for new game panel
    '''

    CANCEL = 0
    ACCEPT = 1

    @abstractmethod
    def update(self, enabled_options, number_of_stars):
        '''
        Called when panel parameters change
        '''


class NewGamePresenter(Presenter):

    '''
    Behaviors for new game panel
    '''

    view_class = NewGameView

    model_class = NewGameModel

    def _initialize_presenter(self):
        self._view.update(
            enabled_options={NewGameView.CANCEL},
            number_of_stars=self._model.number_of_stars)
