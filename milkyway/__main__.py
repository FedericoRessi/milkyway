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
    logger = logging.getLogger('milkyway')
    logger.setLevel(logging.DEBUG)

    logger.info('Initializing Milkyway...')
    application = Application(argv)

    logger.info('Running Milkyway...')
    application.run()

    logger.info('Quit Milkyway.')
    return 0

if __name__ == '__main__':
    main(sys.argv)
