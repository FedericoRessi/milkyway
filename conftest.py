# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# pylint: disable=invalid-name
# -----------------------------------------------------------------------------

'''

@author: Federico Ressi
'''

import logging
import os
import shelve

import ptknows


logger = logging.getLogger(__name__)


store = shelve.open(os.path.join(os.curdir, 'ptknows.dbm'), writeback=True)


def open_store():
    '''
    Open store for ptknownw
    '''
    return store


def close_store():
    '''
    Close and save store for ptknownw
    '''
    store.sync()
    store.close()

ptknows.register_store(open_store, close_store)
pytest_plugins = ["ptknows", ]
