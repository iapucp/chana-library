from setuptools import setup, find_packages
from codecs import open
from os import path

files = ["files/*"]

setup(
    name='chana',  # Required
    version='0.9',  # Required
    description='A library of NLP tools for the shipibo-konibo language',  # Required

    url='https://github.com/iapucp/chana-library',  # Optional
    author='Jose Pereira',  # Optional
    author_email='jpereira@pucp.edu.pe',  # Optional
    license='MIT',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='nlp shipibo development',  # Optional
    
    packages= ['chana'],  # Required
    package_data = {'chana' : files },
    include_package_data=True,

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Main Page': 'https://chana.inf.pucp.edu.pe',
    },
)