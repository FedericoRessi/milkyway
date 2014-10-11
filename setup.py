'''
Created on Oct 11, 2014

@author: federico
'''

import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys

import milkyway


URL = "https://github.com/FedericoRessi/milkyway"


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="milkyway",
    version=milkyway.__version__,
    author="Federico Ressi",
    author_email="federico.ressi@gmail.com",
    description=("Turn based strategy game from Milky Way galaxy."),

    license='GPL3',
    keywords="strategy game",
    url=URL,
    download_url=URL + "/archive/master.zip",
    packages=['milkyway'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Games",
        "License :: OSI Approved :: GPL3 License",
    ],
    platforms = ["Windows", "Linux", "Mac OS-X"],

    tests_require=['tox'],
    cmdclass = {'test': Tox}
)
