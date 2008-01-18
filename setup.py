#! /usr/bin/env python
# Last Change: Sat Jan 19 12:00 AM 2008 J
# TODO:
#   - check how to handle cmd line build options with distutils and use
#   it in the building process

""" pysamplerate is a small python package to resample audio data in numpy
arrays to a difference sampling rate: it is basically a wrapper around the
Secret Rabbit Code from Erik Castro De Lopo (http://www.mega-nerd.com/SRC/).
This package only makes sense for audio data, and has high quality converters
based on the work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)
    
LICENSE: the license of samplerate is the GPL, as is SRC itself."""

from os.path import join
import os

DISTNAME        = 'pysamplerate' 
DESCRIPTION     = 'A python module to resample audio data at high quality'
MAINTAINER      = 'David Cournapeau',
MAINTAINER_EMAIL= 'david@ar.media.kyoto-u.ac.jp',
URL             = 'http://ar.media.kyoto-u.ac.jp/members/david',
LICENSE         = 'GPL'

from info import _C_SRC_MAJ_VERSION as SAMPLERATE_MAJ_VERSION

# The following is more or less random copy/paste from numpy.distutils ...
from numpy.distutils.system_info import system_info, NotFoundError, dict_append
from numpy.distutils.system_info import so_ext, get_info

class SamplerateNotFoundError(NotFoundError):
    """ samplerate (http://www.mega-nerd.com/SRC/) library not found.
    Directories to search for the libraries can be specified in the
    site.cfg file (section [samplerate]).""" 
    def __str__(self):
        return self.__doc__

class samplerate_info(system_info):
    #variables to override
    section         = 'samplerate'
    notfounderror   = SamplerateNotFoundError
    libname         = 'samplerate'
    header          = 'samplerate.h'

    def __init__(self):
        system_info.__init__(self)

    def calc_info(self):
        """ Compute the informations of the library """
        prefix  = 'lib'

        # Look for the shared library
        samplerate_libs = self.get_libs('samplerate_libs', self.libname) 
        lib_dirs        = self.get_lib_dirs()
        for i in lib_dirs:
            tmp = self.check_libs(i, samplerate_libs)
            if tmp is not None:
                info    = tmp
                break
        else:
            raise self.notfounderror()
                    
        # Look for the header file
        include_dirs    = self.get_include_dirs() 
        inc_dir         = None
        for d in include_dirs:
            p = self.combine_paths(d,self.header)
            if p:
                inc_dir     = os.path.dirname(p[0])
                headername  = os.path.abspath(p[0])
                break
        if inc_dir is not None:
            if so_ext == '.dll':
                # win32 case
                fullname    = prefix + tmp['libraries'][0] + '-' + \
                        str(SAMPLERATE_MAJ_VERSION) + so_ext
            else:
                # All others ?
                fullname    = prefix + tmp['libraries'][0] + so_ext + \
                        '.' + str(SAMPLERATE_MAJ_VERSION) 
            fullname    = os.path.join(info['library_dirs'][0], fullname)
            dict_append(info, include_dirs=[inc_dir], 
                    fullheadloc = headername, 
                    fulllibloc  = fullname) 

        self.set_info(**info)
        return

from header_parser import do_subst_in_file
def configuration(parent_package='',top_path=None, package_name=DISTNAME):
    if os.path.exists('MANIFEST'): os.remove('MANIFEST')
    if os.path.exists('pysamplerate.py'): os.remove('pysamplerate.py')

    # Check that sndfile can be found and get necessary informations
    # (assume only one header and one library file)
    src_info    = samplerate_info()

    src_config  = src_info.get_info()
    headername  = src_config['fullheadloc']
    libname     = src_config['fulllibloc']

    # Now, generate pysndfile.py.in
    from generate_const import generate_enum_dicts
    repdict = generate_enum_dicts(headername)
    repdict['%SHARED_LOCATION%'] = libname
    do_subst_in_file('pysamplerate.py.in', 'pysamplerate.py', repdict)

    # Get version
    from info import version as pysamplerate_version

    from numpy.distutils.misc_util import Configuration
    config = Configuration(package_name,parent_package,top_path,
             version     = pysamplerate_version,
             maintainer  = MAINTAINER,
             maintainer_email = MAINTAINER_EMAIL,
             description = DESCRIPTION,
             url    = URL,
             license = LICENSE)
    # config.add_data_dir('tests')
    # config.add_data_dir('test_data')

    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(configuration=configuration)
