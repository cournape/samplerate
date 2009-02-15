# cython: embedsignature=True
import numpy as np
import warnings
import copy

cimport numpy as cnp
cimport stdlib
from samplerate cimport *

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
    object PyString_FromStringAndSize(char *v, int len)

_CONVERTOR_TYPE = {
        'sinc_best'         : SRC_SINC_BEST_QUALITY,
        'sinc_medium'       : SRC_SINC_MEDIUM_QUALITY,
        'sinc_fastest'      : SRC_SINC_FASTEST,
        'zero_order_hold'   : SRC_ZERO_ORDER_HOLD,
        'linear'            : SRC_LINEAR
}

def resample(cnp.ndarray input, r, type, verbose=False):
    """Resample the input array using the given converter type, with a ratio r
    (ie the resulting array will have a length ~ r * input's length).
    
    Arguments
    ---------
    input: array
        input data
    r: float
        ratio
    type: str
        convert type

    Note
    ----
    If input has rank 1, than all data are used. If rank is 2, 
    the number columns will be assumed to be the number of channels.
    """
    cdef cnp.ndarray[cnp.float32_t, ndim=2] ty
    cdef long osz, nframes
    cdef int nc, st
    cdef SRC_DATA sr

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

    osz  = <long>(r * nframes + 1)
    input = np.require(input, requirements='C', dtype=np.float32)
    ty = np.empty((nframes, nc), dtype=np.float32, order='C')

    sr.data_in = <float*>input.data
    sr.data_out = <float*>ty.data
    sr.input_frames = nframes
    sr.output_frames = osz
    sr.src_ratio = r

    st = src_simple(&sr, _CONVERTOR_TYPE[type], nc)
    if not st == 0:
        raise RuntimeError('Error while calling wrapper, return status is %d (should be 0)' % st)

    info =  "samplerate info: "
    info +=  "\n\t%d frames used from input" % sr.input_frames_used
    info += "\n\t%d frames written in output" % sr.output_frames_gen
    
    if verbose:
        if not sr.output_frames_gen == osz:
            info    += "\n\toutput has been resized from %ld to %ld" % \
                        (osz, sr.output_frames_gen)
        print info
    
    return ty
