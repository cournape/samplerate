============
Introduction
============

Purpose of samplerate
=====================

Samplerate is a python module to do high quality resampling of audio signals,
using sinc interpolation. Samplerate gives you functionalities similar to
resample in matlab (the actual resampling method may differ, though), and is
intended to be used with numpy arrays.

Acknowledgments
===============

Please note that samplerate is essentially a wrapper around the `Sampling Rate
Conversion library <http://www.mega-nerd.com/SRC/>`_, aka Source Rabbit Code,
the high quality sampling rate convertion library of Erik de Castro Lopo. All
the features of samplerate are his owns, all the bugs mine.
