# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# pylint: disable=protected-access,redefined-outer-name
# -----------------------------------------------------------------------------

'''
Test milkyway package.

@author: Federico Ressi
'''

from pytest import fixture  # pylint: disable=no-name-in-module


@fixture
def module():
    '''
    Milkway module
    '''

    import milkyway
    return milkyway


def test_version_format(module):
    'Package version has following format: A.B.C'

    version = module.__version__.split('.')
    assert len(version) == 3
    for num in version:
        assert num >= 0
