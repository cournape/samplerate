#! /usr/bin/env python
# Last Change: Fri Mar 27 04:00 PM 2009 J
# TODO:
#   - check how to handle cmd line build options with distutils and use
#   it in the building process

"""samplerate is a small python package to resample audio data in numpy arrays
to a difference sampling rate: it is basically a wrapper around the Secret
Rabbit Code from Erik de Castro Lopo (http://www.mega-nerd.com/SRC/).  This
package only makes sense for audio data, and has high quality converters based
on the work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)

LICENSE: the license of samplerate is the GPL, as is SRC itself."""

from os.path import join
import os
import sys

import setuptools
from numpy.distutils.core import setup

SAMPLERATE_MAJ_VERSION = 0

from common import *

def configuration(parent_package='',top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')

    pkg_prefix_dir = os.path.join('scikits', 'samplerate')

    write_version(os.path.join("scikits", "samplerate", "version.py"))
    if os.path.exists(os.path.join("docs", "src")):
        write_version(os.path.join("docs", "src", "samplerate_version.py"))
    write_info(os.path.join("scikits", "samplerate", "info.py"))

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None,parent_package,top_path,
             namespace_packages=['scikits'],
             version=VERSION,
             maintainer=MAINTAINER,
             maintainer_email=MAINTAINER_EMAIL,
             description=DESCRIPTION,
             long_description=LONG_DESCRIPTION,
             url=URL,
             download_url=DOWNLOAD_URL,
             license=LICENSE)

    config.set_options(
            ignore_setup_xxx_py=True,
            assume_default_configuration=True,
            delegate_options_to_subpackages=True,
            quiet=True,
            )

    config.add_subpackage('scikits')
    config.add_data_files('scikits/__init__.py')

    config.add_subpackage(DISTNAME)

    return config

if __name__ == "__main__":
    setup(configuration = configuration,
        name=DISTNAME,
        install_requires = 'numpy', # can also add version specifiers
        namespace_packages = ['scikits'],
        packages = setuptools.find_packages(),
        include_package_data = True,
        #package_data = {'scikits.audiolab': data_files},
        test_suite = "tester", # for python setup.py test
        zip_safe = False, # zip egg are a pain
        #FIXME url, download_url, ext_modules
        classifiers = CLASSIFIERS,
    )
