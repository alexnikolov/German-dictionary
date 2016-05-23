from setuptools import setup, find_packages

setup(
    name='German dictionary',

    version='1.0',

    description='A dictionary for german language enthusiasts',

    url='https://github.com/alexnikolov/German-dictionary',

    author='Alex Nikolov',
    author_email='alexnickolow@gmail.com',

    license='GNU GPL v2',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',

        'Programming Language :: Python :: 3 :: Only',

        'Topic :: Education',


    ],

    keywords='german dictionary',

    packages=['dictionary'],
)