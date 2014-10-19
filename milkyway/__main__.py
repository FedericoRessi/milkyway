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
    logging.basicConfig()
    milkyway_logger = logging.getLogger('milkyway')
    milkyway_logger.setLevel(logging.DEBUG)

    milkyway_logger.info('Initializing Milkyway...')
    application = Application(argv)

    milkyway_logger.info('Running Milkyway...')
    application.run()

    milkyway_logger.info('Quit Milkyway.')
    return 0

if __name__ == '__main__':
    main(sys.argv)
