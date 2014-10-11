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
Test module for milkyway package.

@author: Federico Ressi
'''

from __future__ import division

import logging

import milkyway


logger = logging.getLogger(__name__)


def test_version_format():
    'Package version has following format: A.B.C'

    version = milkyway.__version__.split('.')
    assert len(version) == 3
    for num in version:
        assert num >= 0
