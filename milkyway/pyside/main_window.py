# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
# -----------------------------------------------------------------------------
'''

@author: Federico Ressi
'''

from PySide.QtGui import QWidget, QHBoxLayout, QStackedLayout, QVBoxLayout,\
    QPushButton, QLabel
import logging

import milkyway
from milkyway.pyside.new_game import NewGamePanel
from milkyway.ui.main_window import MainWindowView, MainWindowModel
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class MainWindow(MainWindowView):

    '''
    Main window view
    '''

    widget = None
    _layout = None

    _main_menu = None
    _main_menu_buttons = None

    def _initialize_view(self):
        presenter = self._presenter

        self.widget = window = QWidget()
        window.setWindowTitle(milkyway.LEMMA)

        self._layout = window_layout = QStackedLayout()
        window.setLayout(window_layout)

        self._main_menu = main_menu = QWidget(window)
        window_layout.addWidget(main_menu)
        main_menu_v_layout = QHBoxLayout()
        main_menu.setLayout(main_menu_v_layout)

        main_menu_v_layout.addStretch(20)
        main_menu_v_layout.addWidget(QLabel(milkyway.LEMMA))

        main_menu_layout = QVBoxLayout()
        main_menu_v_layout.addLayout(main_menu_layout)
        main_menu_v_layout.addStretch(20)

        main_menu_layout.addStretch()
        self._main_menu_buttons = buttons = {}

        buttons[MainWindowModel.CONTINUE_GAME] = continue_game = QPushButton(
            'Continue game')
        main_menu_layout.addWidget(continue_game)
        continue_game.clicked.connect(presenter.continue_game_clicked)

        buttons[MainWindowModel.NEW_GAME] = new_game = QPushButton('New game')
        main_menu_layout.addWidget(new_game)
        new_game.clicked.connect(presenter.new_game_clicked)

        buttons[MainWindowModel.LOAD_GAME] = load_game = QPushButton(
            'Load game')
        main_menu_layout.addWidget(load_game)
        load_game.clicked.connect(presenter.load_game_clicked)

        buttons[MainWindowModel.SAVE_GAME] = save_game = QPushButton(
            'Save Game')
        main_menu_layout.addWidget(save_game)
        save_game.clicked.connect(presenter.save_game_clicked)

        buttons[MainWindowModel.QUIT] = quit_button = QPushButton('Quit')
        main_menu_layout.addWidget(quit_button)
        quit_button.clicked.connect(presenter.quit_clicked)

        main_menu_layout.addStretch()

    def _dispose_view(self):
        self.widget.close()
        del self.widget
        del self._layout
        del self._main_menu
        del self._main_menu_buttons

    def show(self):
        self.widget.show()

    def show_main_menu(self, enabled_options):

        for option, button in self._main_menu_buttons.iteritems():
            button.setEnabled(option in enabled_options)

        self._layout.setCurrentWidget(self._main_menu)

    def show_new_game(self):
        panel = NewGamePanel(parent=self)
        self._layout.addWidget(panel.widget)
        presenter = self._presenter
        panel.cancel.clicked.connect(presenter.cancel_clicked)
        panel.accept.clicked.connect(presenter.accept_clicked)
        self._layout.setCurrentWidget(panel.widget)
