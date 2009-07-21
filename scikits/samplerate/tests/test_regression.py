import numpy as np
from numpy.testing import *
from scikits.samplerate import resample

def test_mono():
    fs = 16000.
    fr = 8000.

    f0 = 440.

    # Create a small stereo audio array with dephased channel
    x = np.sin(2 * np.pi * f0/fs * np.arange(0, 2 * fs))

    # Upsampled reference
    z_r = np.sin(2 * np.pi * f0/fr * np.arange(0, 2 * fr))

    z = resample(x, fr /fs, 'sinc_best')

    assert np.max(np.abs(z_r[10:-1] - z[10:])) < 1e-2

def test_multi_channel():
    fs = 16000.
    fr = 8000.

    f0 = 440.

    # Create a small stereo audio array with dephased channel
    xleft = np.sin(2 * np.pi * f0/fs * np.arange(0, 2 * fs))
    xright = np.cos(2 * np.pi * f0/fs * np.arange(0, 2 * fs))
    y = np.empty((xleft.size, 2), np.float)
    y[:,0] = xleft
    y[:,1] = xright

    # Upsampled reference
    z_rleft = np.sin(2 * np.pi * f0/fr * np.arange(0, 2 * fr))
    z_rright = np.cos(2 * np.pi * f0/fr * np.arange(0, 2 * fr))
    z_r = np.vstack((z_rleft, z_rright)).T

    z = resample(y, fr /fs, 'sinc_best')

    assert np.max(np.abs(z_r[100:-100] - z[100:-99])) < 1e-2
