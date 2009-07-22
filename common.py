descr   = """\
Samplerate is a small python package to do high quality audio resampling for
data in numpy arrays; IOW, it is a matlab resample replacement.

Samplerate is a wrapper around the Secret Rabbit Code from Erik de Castro Lopo
(http://www.mega-nerd.com/SRC/), which has high quality converters based on the
work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)
"""

DISTNAME            = 'scikits.samplerate'
DESCRIPTION         = 'A python module for high quality audio resampling'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'David Cournapeau'
MAINTAINER_EMAIL    = 'david@ar.media.kyoto-u.ac.jp'
URL                 = 'http://www.ar.media.kyoto-u.ac.jp/members/david/softwares/samplerate'
LICENSE             = 'GPL'
DOWNLOAD_URL        = 'http://pypi.python.org/pypi/scikits.samplerate'

MAJOR = 0
MINOR = 3
MICRO = 3
DEV = False

CLASSIFIERS = ['Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering']

def build_verstring():
    return '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def build_fverstring():
    if DEV:
        return build_verstring() + '.dev'
    else:
        return build_verstring()

def write_version(fname):
    f = open(fname, "w")
    f.writelines("short_version = '%s'\n" % build_verstring())
    f.writelines("dev =%s\n" % DEV)
    f.writelines("version = '%s'\n" % build_fverstring())
    f.close()

def write_info(fname):
    f = open(fname, "w")
    f.writelines("# THIS FILE IS GENERATED FROM THE SETUP.PY. DO NOT EDIT.\n")
    f.writelines('"""%s"""' % descr)
    f.writelines("""
# version of the python module (compatibility -> use
# scikits.samplerate.version.version instead, to be consistent with numpy)
from version import short_version as version
ignore  = False""")
    f.close()

VERSION = build_fverstring()
INSTALL_REQUIRE = 'numpy'
