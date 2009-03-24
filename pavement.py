import os
import subprocess
import sys
import shutil

import sphinx

import setuptools
import distutils
import numpy.distutils

try:
    from paver.tasks import VERSION as _PVER
    if not _PVER >= '1.0':
        raise RuntimeError("paver version >= 1.0 required (was %s)" % _PVER)
except ImportError, e:
    raise RuntimeError("paver version >= 1.0 required")

import paver
import paver.doctools
import paver.path
from paver.easy import options, Bunch, task, needs, dry
from paver.setuputils import setup

import common

setup(name=common.DISTNAME,
        namespace_packages=['scikits'],
        packages=setuptools.find_packages(),
        install_requires=common.INSTALL_REQUIRE,
        version=common.VERSION,
        include_package_data=True)

options(sphinx=Bunch(builddir="build", sourcedir="src"))

def macosx_version():
    st = subprocess.Popen(["sw_vers"], stdout=subprocess.PIPE)
    out = st.stdout.readlines()
    import re
    ver = re.compile("ProductVersion:\s+([0-9]+)\.([0-9]+)\.([0-9]+)")
    for i in out:
        m = ver.match(i)
        if m:
            return m.groups()

def mpkg_name():
    maj, min = macosx_version()[:2]
    pyver = ".".join([str(i) for i in sys.version_info[:2]])
    return "scikits.samplerate-%s-py%s-macosx%s.%s.mpkg" % (common.build_fverstring(),
                            pyver, maj, min)
@task
#@needs(['latex', 'html'])
def dmg():
    builddir = paver.path.path("build") / "dmg"
    builddir.rmtree()
    builddir.mkdir()

    # Copy mpkg into image source
    mpkg_n = mpkg_name()
    mpkg = paver.path.path("dist") / mpkg_n
    mpkg.copytree(builddir / mpkg_n)

    # Copy docs into image source
    doc_root = paver.path.path(builddir) / "docs"
    html_docs = paver.path.path("docs") / "html"
    pdf_docs = paver.path.path("docs") / "pdf" / "samplerate.pdf"
    html_docs.copytree(doc_root / "html")
    pdf_docs.copy(doc_root / "samplerate.pdf")

    # Build the dmg
    image_name = "samplerate-%s.dmg" % common.build_fverstring()
    image = paver.path.path(image_name)
    image.remove()
    cmd = ["hdiutil", "create", image_name, "-srcdir", str(builddir)]
    subprocess.Popen(cmd)
#options.setup.package_data =
#    setuputils.find_package_data("scikits/samplerate",
#                                 package="scikits/samplerate",
#                                 only_in_packages=False)

if paver.doctools.has_sphinx:
    def _latex_paths():
        """look up the options that determine where all of the files are."""
        opts = options
        docroot = paver.path.path(opts.get('docroot', 'docs'))
        if not docroot.exists():
            raise BuildFailure("Sphinx documentation root (%s) does not exist."
                    % docroot)
        builddir = docroot / opts.get("builddir", ".build")
        builddir.mkdir()
        srcdir = docroot / opts.get("sourcedir", "")
        if not srcdir.exists():
            raise BuildFailure("Sphinx source file dir (%s) does not exist"
                    % srcdir)
        latexdir = builddir / "latex"
        latexdir.mkdir()
        return Bunch(locals())

    @task
    def latex():
        """Build Audiolab's documentation and install it into
        scikits/samplerate/docs"""
        paths = _latex_paths()
        sphinxopts = ['', '-b', 'latex', paths.srcdir, paths.latexdir]
        dry("sphinx-build %s" % (" ".join(sphinxopts),), sphinx.main, sphinxopts)
        def build_latex():
            subprocess.call(["make", "all-pdf"], cwd=paths.latexdir)
        dry("Build pdf doc", build_latex)
        destdir = paver.path.path("docs") / "pdf"
        destdir.rmtree()
        destdir.makedirs()
        pdf = paths.latexdir / "samplerate.pdf"
        pdf.move(destdir)

    @task
    @needs(['paver.doctools.html'])
    def html_build():
        """Build Audiolab's html documentation."""
        pass

    @task
    @needs(['html_build'])
    def html():
        """Build Audiolab's documentation and install it into
        scikits/samplerate/docs"""
        builtdocs = paver.path.path("docs") / options.sphinx.builddir / "html"
        destdir = paver.path.path("docs") / "html"
        destdir.rmtree()
        builtdocs.move(destdir)

    @task
    @needs(['html', 'latex'])
    def doc():
        pass

    @task
    @needs('setuptools.command.sdist')
    def sdist(options):
        """Build tarball."""
        pass

    @task
    @needs('doc', 'paver.sdist')
    def release_sdist(options):
        """Build doc + tarball."""
        pass