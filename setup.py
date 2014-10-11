'''
Created on Oct 11, 2014

@author: federico
'''

import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import milkyway


URL = "https://github.com/FedericoRessi/milkyway"


class Tox(TestCommand):  # pylint: disable=too-many-public-methods

    '''
    Command to be used for python setup.py test
    '''

    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    tox_args = None
    test_args = None
    test_suite = False

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
        tox.cmdline(args=shlex.split(self.tox_args))


def read(filename):
    '''
    Reads a text file
    '''

    return open(os.path.join(os.path.dirname(__file__), filename)).read()


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

    # package content
    packages=find_packages(),

    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Games",
        "License :: OSI Approved :: GPL3 License",
    ],
    platforms = ["Windows", "Linux", "Mac OS-X"],

    # TOX integration
    tests_require=['tox'],
    cmdclass = {'test': Tox})
