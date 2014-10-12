# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''

@author: Federico Ressi
'''

from PySide.QtGui import QWidget, QHBoxLayout, QVBoxLayout, QPushButton
import logging

from milkyway.ui.new_game import NewGameView, NewGamePresenter, NewGameModel

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class NewGamePanel(NewGameView):

    '''
    Panel for new game creation
    '''

    widget = None
    _layout = None

    buttons = None

    def _create_presenter(self):
        return NewGamePresenter(self)

    def _initialize_view(self):
        '''
        Setup panel widgets
        '''
        self.widget = panel = QWidget(self._parent.widget)

        self._layout = layout = QVBoxLayout()
        panel.setLayout(layout)

        layout.addStretch()
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        bottom_layout.addStretch()
        self.buttons = buttons = {}

        buttons[NewGameModel.CANCEL] = cancel_button = QPushButton('Cancel')
        bottom_layout.addWidget(cancel_button)

        buttons[NewGameModel.ACCEPT] = accept_button = QPushButton('Accept')
        bottom_layout.addWidget(accept_button)

    def _dispose_view(self):
        '''
        Dispose panel widgets
        '''
        del self._layout
        del self.widget
        del self.buttons

    def update(self, enabled_options, number_of_stars):
        '''
        Update panel parameters
        '''
        for option, button in self.buttons.iteritems():
            button.setEnabled(option in enabled_options)

    @property
    def cancel(self):
        '''
        Cancel button
        '''

        return self.buttons[NewGameModel.CANCEL]

    @property
    def accept(self):
        '''
        Accept button
        '''

        return self.buttons[NewGameModel.ACCEPT]
