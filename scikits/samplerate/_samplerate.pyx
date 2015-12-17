# cython: embedsignature=True
import numpy as np
import warnings
import copy

cimport numpy as cnp
from libc.string cimport strlen
from .samplerate cimport *

cdef extern from *:
    ctypedef char* const_char_ptr "const char*"

cdef extern from "samplerate.h":
    cdef struct SRC_DATA:
        float * data_in
        float * data_out
        long int input_frames
        long int output_frames
        long int input_frames_used
        long int output_frames_gen
        int end_of_input
        double src_ratio
    ctypedef SRC_DATA SRC_DATA

cdef extern from "Python.h":
    object PyUnicode_FromStringAndSize(char *v, int len)

_CONVERTOR_TYPE = {
        'sinc_best'         : SRC_SINC_BEST_QUALITY,
        'sinc_medium'       : SRC_SINC_MEDIUM_QUALITY,
        'sinc_fastest'      : SRC_SINC_FASTEST,
        'zero_order_hold'   : SRC_ZERO_ORDER_HOLD,
        'linear'            : SRC_LINEAR
}

def src_version_str():
    """
    Return version string of SRC.
    """
    cdef int st
    cdef const_char_ptr b

    b = src_get_version()
    return PyUnicode_FromStringAndSize(b, strlen(b))

def available_convertors():
    """
    Return the list of available convertor.
    """
    return _CONVERTOR_TYPE.keys()

def convertor_description(type):
    """
    Return a detailed description of the given convertor type.

    Parameters
    ----------
    type : str
        resample type (see Notes).

    Returns
    -------
    descr : str
        String describing the given convertor.
    """
    cdef const_char_ptr b

    if not type in _CONVERTOR_TYPE.keys():
        raise ValueError("convert type %s unrecognized" % type)

    b = src_get_description(_CONVERTOR_TYPE[type])
    return PyUnicode_FromStringAndSize(b, strlen(b))

def resample(cnp.ndarray input, r, type, verbose=False):
    """
    Resample the input array using the given converter type, with a ratio r
    (ie the resulting array will have a length ~ r * input's length).

    Parameters
    ----------
    input: array
        input data
    r: float
        ratio
    type: str
        resample type (see Note)

    Returns
    -------
    output: array
        output data, whose size is approximately r * input.size

    Notes
    -----
    If input has rank 1, than all data are used, and are assumed to be from a
    mono signal. If rank is 2, the number columns will be assumed to be the
    number of channels.

    The list of convertor types is available from the function
    available_convertors.

    Only sinc_*-based interpolation provide good quality; linear and
    zero_order_hold should be avoided as much as possible, and be used only
    when speed is critical.
    """
    cdef long osz, nframes, input_frames_used, output_frames_gen
    cdef int nc, st

    if input.ndim == 2:
        nframes = input.shape[0]
        nc = input.shape[1]
    elif input.ndim == 1:
        nc = 1
        nframes = input.size
    else:
        raise ValueError("rank > 2 not supported yet")

    if not type in _CONVERTOR_TYPE.keys():
        raise ValueError("convert type %s unrecognized" % type)

    osz  = <long>(r * nframes - 1)
    input = np.require(input, requirements='C', dtype=np.float32)

    if nc == 1:
        st, ty, input_frames_used, output_frames_gen \
                = _resample_mono(input, nframes, osz, r, _CONVERTOR_TYPE[type])
    else:
        st, ty, input_frames_used, output_frames_gen \
                = _resample_multi_channels(input, nframes, osz, r, _CONVERTOR_TYPE[type], nc)
    if not st == 0:
        raise RuntimeError('Error while calling wrapper, return status is %d (should be 0)' % st)

    if verbose:
        info =  "samplerate info: "
        info +=  "\n\t%d frames used from input" % input_frames_used
        info += "\n\t%d frames written in output" % output_frames_gen

        if not output_frames_gen == osz:
            info += "\n\toutput has been resized from %ld to %ld" % \
                    (osz, output_frames_gen)
            print(info)

    return ty

cdef _resample_mono(cnp.ndarray input, long niframes, long noframes, 
        double r, int type):
    cdef cnp.ndarray[cnp.float32_t, ndim=1] ty
    cdef SRC_DATA sr

    ty = np.empty(noframes, dtype=np.float32, order='C')

    sr.data_in = <float*>input.data
    sr.data_out = <float*>ty.data
    sr.input_frames = niframes
    sr.output_frames = noframes
    sr.src_ratio = r

    return src_simple(&sr, type, 1), ty, sr.input_frames_used, sr.output_frames_gen

cdef _resample_multi_channels(cnp.ndarray input, long niframes, long noframes,
        double r, int type, int nc):
    cdef cnp.ndarray[cnp.float32_t, ndim=2] ty
    cdef SRC_DATA sr

    ty = np.empty((noframes, nc), dtype=np.float32, order='C')

    sr.data_in = <float*>input.data
    sr.data_out = <float*>ty.data
    sr.input_frames = niframes
    sr.output_frames = noframes
    sr.src_ratio = r

    return src_simple(&sr, type, nc), ty, sr.input_frames_used, sr.output_frames_gen
