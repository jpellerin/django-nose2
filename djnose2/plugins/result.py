from nose2 import events


class DjNose2Result(events.Plugin):
    alwaysOn = True
    configSection = 'django-nose2-result'

    def pluginsLoaded(self, event):
        self.session.djnose2_result = {'failed': 0, 'error': 0}

    def reportFailure(self, event):
        self.session.djnose2_result['failed'] += 1

    def reportError(self, event):
        self.session.djnose2_result['error'] += 1

