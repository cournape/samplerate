=========================
Download and installation
=========================

Supported platforms
===================

Samplerate has been run succesfully on the following platforms:

    - linux ubuntu (32 and 64 bits) and RHEL 5 (32 and 64 bits)
    - windows XP (32 bits)
    - Mac OS X (10.5, intel)

I would be interested to hear anyone who succeesfully used it on other
platforms.

Download
========

Releases are available on Pypi:

        http://pypi.python.org/pypi/scikits.samplerate/

Samplerate is part of scikits, and its source are in a git repository,
available on `github <http://github.com/cournape/samplerate/tree/master>`_.

Install from binaries
=====================

Requirements
------------

To install the binaries, samplerate requires the following softwares:

 - a python interpreter.
 - numpy (any version >= 1.2 should work).

Binaries
--------

Binaries for Mac OS X and Windows are provided on Pypi - they are statically
linked to SRC (so that you don't need to install your own version of SRC
first). If you are not familiar with building from sources, you are strongly
advised to use those.

Installation from sources
=========================

Requirements
------------

samplerate requires the following softwares:

 - a python interpreter.
 - Source Code Rabbit (SRC)
 - numpy (any version >= 1.2 should work).
 - setuptools

On Ubuntu, you can install the dependencies as follow::

        sudo apt-get install python-dev python-numpy python-setuptools libsamplerate0-dev

Build
-----

For unix users, if SRC is installed in standart location (eg /usr/lib,
/usr/local/lib), the installer should be able to find them automatically, and
you only need to do a "python setup.py install". In other cases, you need to
create a file site.cfg to set the location of SRC and its header (there are
site.cfg examples which should give you an idea how to use them on your
platform).

License
=======

Samplerate is released under the GPL, which forces you to release back the
modifications you may make in the version of samplerate you are distributing,

Audiolab is under the GPL because SRC itself is under the GPL, and as such, a
BSD python wrapper is of little value.
