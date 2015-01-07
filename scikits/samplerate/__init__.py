#! /usr/bin/env python
# Last Change: Thu Mar 26 01:00 AM 2009 J

from .info import __doc__

from ._samplerate import resample, available_convertors, src_version_str, \
    convertor_description
from .version import version as _version
__version__ = _version

__all__ = filter(lambda s:not s.startswith('_'),dir())

from numpy.testing import Tester

test = Tester().test
bench = Tester().bench

