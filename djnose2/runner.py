import sys

from contextlib import contextmanager
import logging

from django.test import simple
from nose2.main import discover


log = logging.getLogger(__name__)


class TestRunner(simple.DjangoTestSuiteRunner):

    err_count = 0
    _hooks = ('startTestRun', 'reportFailure', 'reportError')

    def hooks(self):
        return [(hook, self) for hook in self._hooks]

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        log.debug('Running tests with nose2')
        self.extra_tests = extra_tests
        with self.test_environment():
            argv = self.make_argv(test_labels)
            discover(argv=argv, exit=False, extraHooks=self.hooks())
            return self.err_count

    def make_argv(self, test_labels):
        argv = ['nose2']
        argv.extend(['-v'] * (self.verbosity - 1))

        if self.failfast:
            argv.append('-F')

        # keep nose2 args separate from django/manage args
        if '--' in sys.argv:
            argv.extend(sys.argv[sys.argv.index('--')+1:])

        if test_labels:
            argv.extend([t for t in test_labels if not t.startswith('-')])

        return argv

    @contextmanager
    def test_environment(self):
        self.setup_test_environment()
        old_config = self.setup_databases()
        log.debug("Django test environment set up")
        try:
            yield
        finally:
            self.teardown_databases(old_config)
            self.teardown_test_environment()
            log.debug("Django test environment torn down")

    # plugin hooks the runner handles
    def startTestRun(self, event):
        if self.extra_tests is None:
            return
        for test in self.extra_tests:
            event.suite.addTest(test)

    def reportFailure(self, event):
        self.err_count += 1

    def reportError(self, event):
        self.reportFailure(event)
