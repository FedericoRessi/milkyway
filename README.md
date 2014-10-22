Milky Way
=========

Turn based strategy game from Milky Way galaxy


Overview
--------

The project is still starting. I'm searching for collaborators.


Getting started
---------------

Download source code from [GitHub page](https://github.com/FedericoRessi/milkyway)

```bash
git clone https://github.com/FedericoRessi/milkyway.git 
```


How to use
----------

There is still nothing to use. Only Python meat for now. ;-)


Writing tests
-------------

MilkWay project would adopt [behavior driven development](http://it.wikipedia.org/wiki/Behavior-driven_development) approach to enforce a top-down design and reduce defelop-test-review-fix cicles for integration funtional testing.
To enforce writing behaviours before data models and views UI follows [model-view-presenter](http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93presenter) design pattern. 

For details about using pytest please:

- for writing functional tests see [pytest-bdd documentation](https://github.com/olegpidsadnyi/pytest-bdd)
- for creating test fixtures see [pytest documentation](http://pytest.org/latest/fixture.html)
- for mocking objects see [mocking library](http://www.voidspace.org.uk/python/mock/)


Executing tests
---------

To run tests python2.7 and [Tox](http://tox.readthedocs.org/en/latest/install.html) are required.
Tox should download from internet required python packages.
If some error is reported by Tox (red messages), it must be corrected before the change reaches master branch.

**Execute static analisys**

Statick analisys is perfomed using
- [flake8](http://flake8.readthedocs.org/en/2.2.3/)
- [pylint](http://www.pylint.org/)

**Executing static analisys, all tests and code coverage**

Test execution and code coverage is produced using [pytest](http://pytest.org/latest/)


**Executing all above**

```bash
tox
```

**Integration server**

Travis CI: [![Build Status](https://travis-ci.org/FedericoRessi/milkyway.svg?branch=master)](https://travis-ci.org/FedericoRessi/milkyway)

**Coverage history**

Coveralls: [![Coverage Status](https://coveralls.io/repos/FedericoRessi/milkyway/badge.png?branch=master)](https://coveralls.io/r/FedericoRessi/milkyway?branch=master)
