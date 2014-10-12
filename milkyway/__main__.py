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


logger = logging.getLogger(__name__)


def main(argv):
    from milkyway.pyside.application import Application
    application = Application(argv)
    application.run()

if __name__ == '__main__':
    main(sys.argv)
