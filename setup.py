from pathlib import Path
from setuptools import setup

HERE = Path(__file__).parent

README = (HERE / 'README.md').read_text()

setup(
        name='txtv',
        version='1.0.0',
        description='CLI for reading swedish text-tv',
        long_description=README,
        long_description_content_type='text/markdown',
        url='https://github.com/voidcase/txtv',
        author='Isak Lindhé',
        author_email='isak.e.lindhe@gmail.com',
        license='GPLv3+',
        py_modules=['txtv'],
        packages=setuptools.find_packages(),
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            ],
        install_requires=[
            'beautifulsoup4',
            'colorama',
            'requests',
        ],
        entry_points={
            'console_scripts': [
                'txtv=txtv.txtv:run',
            ],
        }
)
