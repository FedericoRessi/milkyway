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

@author: federico
'''

from __future__ import division

import mock

from milkyway.ui.presenter import Presenter


def test_constructor():
    view = mock.Mock()
    model = mock.Mock()

    presenter = Presenter(view, model)

    assert view is presenter._view
    assert model is presenter._model
