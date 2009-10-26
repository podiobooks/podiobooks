import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "podiobooks",
    version = "1.0",
    url = 'http://github.com/ctmiller/podiobooks',
    license = 'CCPL',
    description = "Free Audiobook Management Site",
    long_description = read('README'),

    author = 'PodioBooks Team',
    author_email = 'feedback@podiobooks.com',

    packages = find_packages('src'),
    package_dir = {'': 'src'},

    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: CCPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
