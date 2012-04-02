import os
from setuptools import setup, find_packages # FIXME

PARAMS = {}
README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
    'Operating System :: OS Independent',
    'Topic :: Software Development :: Libraries',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Software Development :: Testing',
]
KEYWORDS = ['unittest', 'testing', 'tests', 'django']

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    PARAMS['packages'] = 'djnose2'
else:
    PARAMS['packages'] = find_packages()
    PARAMS['install_requires'] = ['Django>=1.2,', 'nose2>=0.3']



setup(
    name='django-nose2',
    author='Jason Pellerin',
    author_email='jpellerin+nose@gmail.com',
    version='0.1',
    url='https://github.com/jpellerin/django-nose2',
    description='Test runner for django that runs tests with nose2',
    long_description=README,
    **PARAMS
    )
