import numpy as np
import pylab as plt
from scikits.samplerate import resample

fs  = 44100.
fr  = 48000.
# Signal to resample
sins    = np.sin(2 * np.pi * 1000/fs * np.arange(0, fs * 2))
# Ideal resampled signal
idsin   = np.sin(2 * np.pi * 1000/fr * np.arange(0, fr * 2))

conv1   = resample(sins, fr/fs, 'linear')
conv3   = resample(sins, fr/fs, 'sinc_best')

err1    = conv1[fr:fr+2000] - idsin[fr:fr+2000]
err3    = conv3[fr:fr+2000] - idsin[fr:fr+2000]

plt.subplot(3, 1, 1)
plt.plot(idsin[fs:fs+2000])
plt.title('Resampler residual quality comparison')

plt.subplot(3, 1, 2)
plt.plot(err1)
plt.ylabel('Linear')

plt.subplot(3, 1, 3)
plt.plot(err3)
plt.ylabel('Sinc')

plt.savefig('example1.png', dpi = 100)
