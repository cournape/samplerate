"""samplerate is a small python package to resample audio data in numpy arrays
to a difference sampling rate: it is basically a wrapper around the Secret
Rabbit Code from Erik Castro De Lopo (http://www.mega-nerd.com/SRC/).  This
package only makes sense for audio data, and has high quality converters based
on the work of J.O Smith from CCRMA (see
http://ccrma.stanford.edu/~jos/resample/optfir.pdf)
    
2006, David Cournapeau

LICENSE: the license of samplerate is GPL, as SRC itself."""

# version of the python module
version                 = '0.1'
# version of the SRC library
_C_SRC_MAJ_VERSION      = 0

ignore  = False
