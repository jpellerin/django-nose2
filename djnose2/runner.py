import sys

from contextlib import contextmanager
import logging

from django.test import simple
from nose2.main import PluggableTestProgram


class TestRunner(simple.DjangoTestSuiteRunner):

    default_plugins = [
        'djnose2.plugins.result',
        ]

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.extra_tests = extra_tests
        with self.test_environment():
            argv = self.make_argv(test_labels)
            proc = TestProgram(argv=argv, module=None, exit=False,
                               plugins=self.default_plugins,
                               hooks=[('startTestRun', self)])
            stor = getattr(proc.session, 'djnose2_result', {})
            return stor.get('failed', 0) + stor.get('error', 0)

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
        try:
            yield
        finally:
            self.teardown_databases(old_config)
            self.teardown_test_environment()

    # plugin hooks I handle myself
    def startTestRun(self, event):
        if self.extra_tests is None:
            return
        for test in self.extra_tests:
            event.suite.addTest(test)


class TestProgram(PluggableTestProgram):
    def __init__(self, **kw):
        self.hooks = kw.pop('hooks', [])
        super(TestProgram, self).__init__(**kw)

    def loadPlugins(self):
        super(TestProgram, self).loadPlugins()
        for method_name, call in self.hooks:
            self.session.hooks.register(method_name, call)
