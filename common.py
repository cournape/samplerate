descr   = """\
Samplerate is a small python package to resample audio data in numpy arrays to
a different sampling rate: it is basically a wrapper around the Secret Rabbit
Code from Erik Castro De Lopo (http://www.mega-nerd.com/SRC/).  This package
only makes sense for audio data, and has high quality converters based on the
work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)

LICENSE: the license of samplerate is the GPL, as is SRC itself.
"""

DISTNAME            = 'scikits.samplerate'
DESCRIPTION         = 'A python module for high quality audio resampling'
LONG_DESCRIPTION    = descr
MAINTAINER          = 'David Cournapeau'
MAINTAINER_EMAIL    = 'david@ar.media.kyoto-u.ac.jp'
URL                 = 'http://www.ar.media.kyoto-u.ac.jp/members/david/softwares/samplerate'
LICENSE             = 'GPL'
DOWNLOAD_URL        = URL

MAJOR = 0
MINOR = 3
MICRO = 1
DEV = True

CLASSIFIERS = ['Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Library or Lesser General '\
        'Public License (LGPL)', 'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering']

def build_verstring():
    return '%d.%d.%d' % (MAJOR, MINOR, MICRO)

def build_fverstring():
    if DEV:
        return build_verstring() + 'dev'
    else:
        return build_verstring()

def write_version(fname):
    f = open(fname, "w")
    f.writelines("version = '%s'\n" % build_verstring())
    f.writelines("dev =%s\n" % DEV)
    f.writelines("full_version = '%s'\n" % build_fverstring())
    f.close()

VERSION = build_fverstring()
INSTALL_REQUIRE = 'numpy'
