# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# pylint: disable=protected-access,redefined-outer-name,invalid-name,
# pylint: disable=missing-docstring
# -----------------------------------------------------------------------------

'''
Test module for milkyway package.

@author: Federico Ressi
'''

from mock import patch, NonCallableMock
from pytest import raises  # pylint: disable=no-name-in-module

from touched_files import LineSet, get_touched_lines, TouchedLinesReader


GIT_DIFF = '''
+++ b/packages/scripts/touched_files.py
@@ -4,0 +5 @@
+from collections import OrderedDict
@@ -6,0 +8 @@ import os
+import numpy
@@ -7,0 +10,146 @@ from subprocess import check_output
+from itertools import imap, izip
+
+
+class LineSet(object):
+    """
+    Class to store a sorted set of source code lines.
'''


def check_output(args):
    'Dummy check_output'

    if args == ('git', 'merge-base', 'origin/master', 'HEAD'):
        return '41e1b3c13995e5614c7a434cd100509b1e927478'

    elif args[:4] == ('git', 'diff', '-U0',
                      '41e1b3c13995e5614c7a434cd100509b1e927478'):

        if args[4:] == tuple():
            return GIT_DIFF

        elif args[4:] == ('--', 'packages/scripts/touched_files.py'):
            return GIT_DIFF

        else:
            return ""

    else:
        raise AssertionError('Unexpected command: {}'.format(args))


@patch('touched_files.check_output', check_output)
def test_get_touched_lines():

    result = get_touched_lines()

    assert {'packages/scripts/touched_files.py':
            LineSet('5, 8, 10-155')} == result


@patch('touched_files.check_output', check_output)
def test_get_touched_lines_with_good_pattern():

    result = get_touched_lines('*.py')

    assert {'packages/scripts/touched_files.py':
            LineSet('5, 8, 10-155')} == result


@patch('touched_files.check_output', check_output)
def test_get_touched_lines_with_bad_pattern():

    result = get_touched_lines('WRONG_PATTERN')

    assert {} == result


# --- LineSetClass ------------------------------------------------------------

def test_init_line_set_from_string():

    lines = LineSet('1, 3, 5-8, 40-60, 89')

    assert [(1, 2), (3, 4), (5, 9), (40, 61), (89, 90)] == list(lines)
    assert '1, 3, 5-8, 40-60, 89' == str(lines)


def test_init_line_set_from_sequence():

    lines = LineSet([(1, 2), (3, 4), (5, 9), (40, 61), (89, 90)])

    assert [(1, 2), (3, 4), (5, 9), (40, 61), (89, 90)] == list(lines)
    assert '1, 3, 5-8, 40-60, 89' == str(lines)


def test_init_line_set_from_nothing():

    lines = LineSet()

    assert [] == list(lines)
    assert '' == str(lines)


def test_init_line_set_from_bad_strings():
    with raises(ValueError):
        LineSet('10, 2')

    with raises(ValueError):
        LineSet('5-3')

    with raises(ValueError):
        LineSet('2-3-4')


def test_repr_line_set():
    assert "LineSet('1, 10')" == repr(LineSet('1, 10'))


def test_intersect_line_sets():
    assert "3-5" == str(LineSet('1-5, 10') & LineSet('3-6, 15-20'))


# --- TouchedLinesReader ------------------------------------------------------

@patch('touched_files.check_output', check_output)
def test_reader_to_stream():
    stream = NonCallableMock()
    reader = TouchedLinesReader()
    reader.fetch(items=['packages/scripts/touched_files.py'])

    reader.to_stream(stream=stream)

    stream.write.assert_called_once_with(
        'packages/scripts/touched_files.py    5, 8, 10-155\n')


@patch('touched_files.check_output', check_output)
def test_fetch_with_valid_items():
    reader = TouchedLinesReader()

    result = reader.fetch(items=['packages/scripts/touched_files.py'])

    assert result
    assert {'packages/scripts/touched_files.py':
            LineSet('5, 8, 10-155')} == reader


@patch('touched_files.check_output', check_output)
def test_fetch_with_invalid_items():
    reader = TouchedLinesReader()

    result = reader.fetch(items=['WrRoooNGfiLE'])

    assert not result
    assert {} == reader


@patch('touched_files.check_output', check_output)
def test_fetch_with_get_item_and_item_is_valid():
    reader = TouchedLinesReader()

    result = reader['packages/scripts/touched_files.py']

    assert '5, 8, 10-155' == str(result)


@patch('touched_files.check_output', check_output)
def test_fetch_with_get_item_and_item_is_invalid():
    reader = TouchedLinesReader()
    with raises(KeyError):
        reader['WrRoooNGfiLE']  # pylint: disable=pointless-statement
