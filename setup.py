from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent

README = (HERE / 'README.md').read_text()

VERSION = '2.0.0'

setup(
        name='txtv',
        version=VERSION,
        description='CLI for reading swedish text-tv',
        long_description=README,
        long_description_content_type='text/markdown',
        url='https://github.com/voidcase/txtv',
        download_url=f'https://github.com/voidcase/txtv/archive/v{VERSION}.tar.gz',
        author='Isak Lindhé',
        author_email='isak.e.lindhe@gmail.com',
        license='GPLv3+',
        py_modules=['txtv'],
        packages=find_packages(),
        python_requires='>=3.6',
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Environment :: Console',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: POSIX',
            'Operating System :: MacOS',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
            'Natural Language :: Swedish',
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
