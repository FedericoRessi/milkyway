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
import sys

from milkyway.pyside.application import Application


logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


def main(argv):
    '''
    Executes Milky Way game
    '''

    application = Application(argv)
    application.run()


if __name__ == '__main__':
    main(sys.argv)
