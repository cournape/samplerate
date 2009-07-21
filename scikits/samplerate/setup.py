import os
import sys

from numpy.distutils.core import setup, Extension
from setuphelp import info_factory, NotFoundError

def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    confgr = Configuration('samplerate', parent_package, top_path)

    # Check that sndfile can be found and get necessary informations
    sf_info = info_factory('samplerate', ['samplerate'], ['samplerate.h'],
                           classname='SamplerateInfo')()
    try:
        sf_config = sf_info.get_info(2)
    except NotFoundError:
        raise NotFoundError("""\
SRC (http://www.mega-nerd.com/SRC/) library not found.  Directories to search
for the libraries can be specified in the site.cfg file, in section
[samplerate].""")

    confgr.add_extension('_samplerate', ['_samplerate.c'], extra_info=sf_config)
    confgr.add_data_dir('tests')

    return confgr

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
