# THIS FILE IS GENERATED FROM THE SETUP.PY. DO NOT EDIT.
"""Samplerate is a small python package to resample audio data in numpy arrays to
a different sampling rate: it is basically a wrapper around the Secret Rabbit
Code from Erik Castro De Lopo (http://www.mega-nerd.com/SRC/).  This package
only makes sense for audio data, and has high quality converters based on the
work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)

LICENSE: the license of samplerate is the GPL, as is SRC itself.
"""
# version of the python module (compatibility -> use
# scikits.samplerate.version.version instead, to be consistent with numpy)
from version import short_version as version
ignore  = False