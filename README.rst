Django nose2 test runner
========================

A test runner for django 1.2 or better that runs tests with nose2.

Usage
-----

In your settings module, set::

  TEST_RUNNER=djnose2.TestRunner

Then ``manage.py test`` will run nose2's test runner.

Notes
-----

Put command-line arguments for the test runner after '--'. For
example, to turn on output buffering::

  manage.py test -v 2 -- -B

(But really, almost all of the time, you'll want to put your nose2
configuration in a config file).
