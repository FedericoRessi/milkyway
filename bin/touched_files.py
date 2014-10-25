#!/usr/bin/python
# -----------------------------------------------------------------------------
# Milky Way - Turn based strategy game from Milky Way galaxy
#
# URL:        https://github.com/FedericoRessi/milkyway/
# License:    GPL3
#
# Created:    {date}
# Modified:   __updated__
# -----------------------------------------------------------------------------
from os.path import dirname

'''

@author: Federico Ressi
'''

from collections import Mapping
from fnmatch import fnmatch
import os
import sys
from subprocess import check_output
from itertools import imap, izip

import numpy


MERGE_BASE_COMMAND = ('git', 'merge-base')

MERGE_BASE_BRANCH_REFERENCE = ('origin/master', 'HEAD')


DIFF_COMMAND = ('git', 'diff')

DIFF_NAMES_COMMAND = DIFF_COMMAND + ('--names-only',)


def main(argv):
    'Draft of a main function.'
    # TODO: implement better argument parsing
    if len(argv) > 1:
        include_pattern = argv[1]

    else:
        include_pattern = None

    get_touched_lines(include_pattern=include_pattern).to_stream()


def get_touched_dirs(
        include_pattern=None, branch_reference=MERGE_BASE_BRANCH_REFERENCE):
    """
    Returns the list of directories that have changed compared to the master.
    """

    touched_files = get_touched_files(
        include_pattern=include_pattern, branch_reference=branch_reference)

    # get a sorted list of all directories where at least a file has changed
    touched_dirs = sorted(imap(dirname, touched_files))

    # remove sub-directories of others
    return [touched
            for i, touched in enumerate(touched_dirs)
            if i == 0 or not touched.startswith(touched_dirs[i - 1])]


def get_touched_files(
        include_pattern=None, branch_reference=MERGE_BASE_BRANCH_REFERENCE):
    """Return the list of files that have changed compared to the master."""
    merge_base = get_merge_base(branch_reference)
    touched_files = check_output(
        DIFF_NAMES_COMMAND + (merge_base,)).splitlines()

    match = _get_filter_function(include_pattern)
    return [touched for touched in touched_files if match(touched)]


def get_merge_base(branch_reference=MERGE_BASE_BRANCH_REFERENCE):
    '''
    Returns the revision id of the last commit of master branch merged on this
    one
    '''
    git_merge_base = MERGE_BASE_COMMAND + branch_reference
    return check_output(git_merge_base).strip()


def get_touched_lines(
        include_pattern=None, branch_reference=MERGE_BASE_BRANCH_REFERENCE):
    """
    Return an ordered dictionary of files that have changed
    compared to the master.
     - keys of the dictionary are file names (strings),
     - values are LineSet instances of touched lines.
    """

    touched_lines = TouchedLinesReader(
        filter_function=_get_filter_function(include_pattern),
        merge_base=get_merge_base(branch_reference))
    touched_lines.fetch()
    return touched_lines


class TouchedLinesReader(Mapping):

    '''
    Maps file names to set of modified lines. When a name of file that is not
    mapped is required, it is fetched to git just in time.

    '''

    _order = None

    def __init__(self, merge_base=None, filter_function=None):
        self._entries = {}
        self._merge_base = merge_base

        if not filter_function:
            filter_function = _not_empty
        assert callable(filter_function)
        self._match_file_name = filter_function

    def fetch(self, items=None):
        '''
        Ask git which files have been modified since last merged commit on
        master branch.
        '''

        touched_lines = []
        file_name = None

        # parse git output
        for line in self._fetch_differences(items):
            # parse line
            fields = line.split()
            if len(fields) > 1 and fields[0] == '+++':

                # this line contains the modified/new file name

                file_name = self._normalize_file_name(fields[1][2:])
                if file_name:
                    # parse differences of this file
                    line_set = LineSet()
                    touched_lines.append((file_name, line_set))

                else:
                    # skip this file
                    _check_coverage()

            elif file_name and len(fields) > 2 and fields[0] == '@@':

                # this line introduces a new block of differences with starting
                # line number and number of lines
                start, stop = self._get_modified_lines_extent(fields)
                if start:
                    line_set.append(start, stop)

            else:
                # irrelevant info
                _check_coverage()

        if touched_lines:
            # Update internal cache
            self._order = None
            self._entries.update(touched_lines)
            return True

        else:
            # No matching file has changed
            return False

    @property
    def merge_base(self):
        '''
        Revision id of the last commit of master branch merged on this one
        '''
        # wake up git only once.
        merge_base = self._merge_base
        if merge_base is None:
            self._merge_base = merge_base = get_merge_base()
        return merge_base

    @merge_base.setter
    def set_merge_base(self, merge_base):
        'Set merge base revision id.'
        self._merge_base = merge_base

    def _fetch_differences(self, items=None):
        'Ask GIT for differences'
        git_diff = ('git', 'diff', '-U0', self.merge_base)
        if items:
            git_diff += ('--',) + tuple(items)
        return check_output(git_diff).splitlines()

    def _normalize_file_name(self, file_name):
        'Parse file name from given line'
        file_name = os.path.normpath(file_name)

        if self._match_file_name(file_name):
            # the name of the file matches given patter
            # prepare a new entry
            return file_name

        else:
            # mark all lines of this file to be skipped
            return None

    @staticmethod
    def _get_modified_lines_extent(fields):
        'Returns the range of modified lines as a tuple: start, stop'

        nums = [int(w) for w in fields[2][1:].split(',', 3)]
        if len(nums) > 1:
            # here we have the first modified line number and
            # the number of modified or new line in the block
            if nums[1]:
                return nums[0], nums[0] + nums[1]

            else:
                # when lines are removed, this number is zero
                return None, None

        else:
            # here we have a single line
            return nums[0], nums[0] + 1

    def __getitem__(self, item):
        path = os.path.normpath(item)
        value = self._entries.get(path, None)
        if value is None:
            self.fetch([item])
        return self._entries[path]

    def __iter__(self):
        order = self._order
        entries = self._entries
        if order is None:
            self._order = order = sorted(
                entries.iterkeys(), key=lambda name: len(entries[name]))
        return iter(order)

    def __len__(self):
        return len(self._entries)

    def to_stream(self, stream=sys.stdout):
        'Prints a list of modified files with touched lines for every one.'
        max_filename_len = 0
        for filename in self:
            max_filename_len = max(max_filename_len, len(filename))

        for filename, lines in self.iteritems():
            space = ' ' * (max_filename_len - len(filename) + 4)
            stream.write(filename + space + str(lines) + '\n')


class LineSet(object):

    """
    Class to store a sorted set of source code lines.
    """

    _starts = None
    _stops = None
    _len = 0

    def __init__(self, sequence_or_string=None):
        if sequence_or_string is None or len(sequence_or_string) == 0:
            self.clear()
        elif isinstance(sequence_or_string, str):
            self.update_from_string(sequence_or_string)
        else:
            self.update_from_sequence(sequence_or_string)

    def clear(self):
        'Erase the set'
        self._starts = []
        self._stops = []
        self._len = 0

    def __iter__(self):
        return izip(self._starts, self._stops)

    def update_from_sequence(self, sequence):
        'Build set from sorted sequences of integer pairs (start, stop)'
        self.clear()
        for start, stop in sequence:
            self.append(start, stop)

    def update_from_string(self, from_string):
        'Build set parsing a string.'
        self.clear()
        start = 0
        stop = 0
        for entry in from_string.split(','):
            for i, value in enumerate(entry.strip().split('-')):
                if i == 0:
                    new_start = int(value)
                    if new_start <= start:
                        raise ValueError(
                            'Start line not greater that previous one: '
                            '{}'.format(entry))
                    start = new_start
                    stop = start + 1

                elif i == 1:
                    new_stop = int(value) + 1
                    if new_stop <= start:
                        raise ValueError(
                            'Stop line not greater that start line: {}'
                            .format(entry))
                    stop = new_stop

                else:
                    raise ValueError(
                        'Too many values in line set entry: {}'.
                        format(entry))

            if start > 0:
                self.append(start, stop)

    def append(self, start, stop):
        '''
        Add a new entry at the end of the set. Please note that entries have '
        to be appended in increasing order.
        '''
        assert start > 0
        assert stop > start, '{} > {}'.format(start, stop)
        self._starts.append(start)
        self._stops.append(stop)
        self._len += stop - start

    def __len__(self):
        return self._len

    def __str__(self):
        return ', '.join(imap(_interval_to_string, self._starts, self._stops))

    def __repr__(self):
        return "LineSet('{!s}')".format(self)

    def __eq__(self, other):
        # pylint: disable=protected-access
        return isinstance(other, LineSet) and self._starts == other._starts and\
            self._stops == other._stops

    def intersect(self, other):
        'Compute the intersection between two line sets.'

        # pylint: disable=protected-access, no-member

        assert isinstance(other, LineSet)

        max_line = max(self._stops[-1], other._stops[-1]) + 1

        self_diffs = numpy.zeros((max_line,), dtype=int)
        self_diffs[self._starts] = 1
        self_diffs[self._stops] = -1
        self_bools = numpy.cumsum(self_diffs)

        other_diffs = numpy.zeros((max_line,), dtype=int)
        other_diffs[other._starts] = 1
        other_diffs[other._stops] = -1
        other_bools = numpy.cumsum(other_diffs)

        result_bools = (self_bools > 0) & (other_bools > 0)
        result_flaat = numpy.nonzero(
            result_bools[:-1] ^ result_bools[1:])[0] + 1

        return LineSet(result_flaat.reshape((len(result_flaat) / 2, 2)))

    __and__ = intersect


def _interval_to_string(start, stop):
    'Converts a block of modified lines to string.'

    if stop - start > 1:
        return '{}-{}'.format(start, stop - 1)

    else:
        return str(start)


def _check_coverage():
    'placeholder used to check coverage of empty branches'


def _get_filter_function(include_pattern):
    'get file name match function given a pattern'

    if include_pattern:

        def _match_pattern(name):
            'Matches some names.'
            return _not_empty(name) and fnmatch(name, include_pattern)

        return _match_pattern

    else:
        return _not_empty


def _not_empty(name):  # pylint: disable=unused-argument
    'Matches all names.'
    return bool(name)


if __name__ == '__main__':
    main(sys.argv)
