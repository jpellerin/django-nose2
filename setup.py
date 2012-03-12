from setuptools import setup, find_packages # FIXME

setup(
    name='django-nose2',
    version='0.1',
    packages=find_packages(),
    install_requires=['Django>=1.2,', 'nose2>=0.2'],
    )
