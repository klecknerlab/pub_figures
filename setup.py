from setuptools import setup

setup(
    name='pub_figures',
    version='0.1',
    description='A python module to configure matplotlib with appropriate settings for generating publication quality plots',
    url='https://github.com/klecknerlab/pub_figures',
    author='Dustin Kleckner',
    author_email='dkleckner@ucmerced.edu',
    license='Apache 2.0 (http://www.apache.org/licenses/LICENSE-2.0)',
    packages=['pub_figures'],
    install_requires=[ #Many of the packages are not in PyPi, so assume the user knows how to isntall them!
        # 'numpy',
        # 'PyQt5',
    ],
)
