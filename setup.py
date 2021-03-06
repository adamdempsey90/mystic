#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2018 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/mystic/blob/master/LICENSE

from __future__ import with_statement
import os
import sys

# set version numbers
stable_version = '0.3.1'
target_version = '0.3.2'
is_release = stable_version == target_version

# check if easy_install is available
try:
#   import __force_distutils__ #XXX: uncomment to force use of distutills
    from setuptools import setup
    has_setuptools = True
except ImportError:
    from distutils.core import setup
    has_setuptools = False

# generate version number
if os.path.exists('mystic/info.py'):
    # is a source distribution, so use existing version
    os.chdir('mystic')
    with open('info.py','r') as f:
        f.readline() # header
        this_version = f.readline().split()[-1].strip("'")
    os.chdir('..')
elif stable_version == target_version:
    # we are building a stable release
    this_version = stable_version
else:
    # we are building a distribution
    this_version = target_version + '.dev0'
    if is_release:
      from datetime import date
      today = "".join(date.isoformat(date.today()).split('-'))
      this_version += "-" + today

# get the license info
with open('LICENSE') as file:
    license_text = file.read()

# generate the readme text
long_description = \
"""---------------------------------------------------------------------------------
mystic: highly-constrained non-convex optimization and uncertainty quantification
---------------------------------------------------------------------------------

About Mystic
============

The ``mystic`` framework provides a collection of optimization algorithms
and tools that allows the user to more robustly (and easily) solve hard
optimization problems. All optimization algorithms included in ``mystic``
provide workflow at the fitting layer, not just access to the algorithms
as function calls. ``mystic`` gives the user fine-grained power to both
monitor and steer optimizations as the fit processes are running.
Optimizers can advance one iteration with ``Step``, or run to completion
with ``Solve``.  Users can customize optimizer stop conditions, where both
compound and user-provided conditions may be used. Optimizers can save
state, can be reconfigured dynamically, and can be restarted from a
saved solver or from a results file.  All solvers can also leverage
parallel computing, either within each iteration or as an ensemble of
solvers.

Where possible, ``mystic`` optimizers share a common interface, and thus can
be easily swapped without the user having to write any new code. ``mystic``
solvers all conform to a solver API, thus also have common method calls
to configure and launch an optimization job. For more details, see
``mystic.abstract_solver``. The API also makes it easy to bind a favorite
3rd party solver into the ``mystic`` framework.

Optimization algorithms in ``mystic`` can accept parameter constraints,
either in the form of penaties (which "penalize" regions of solution
space that violate the constraints), or as constraints (which "constrain" 
the solver to only search in regions of solution space where the
constraints are respected), or both. ``mystic`` provides a large 
selection of constraints, including probabistic and dimensionally
reducing constraints. By providing a robust interface designed to
enable the user to easily configure and control solvers, ``mystic``
greatly reduces the barrier to solving hard optimization problems.

``mystic`` is in active development, so any user feedback, bug reports, comments,
or suggestions are highly appreciated.  A list of known issues is maintained
at http://trac.mystic.cacr.caltech.edu/project/mystic/query.html, with a public
ticket list at https://github.com/uqfoundation/mystic/issues.


Major Features
==============

``mystic`` provides a stock set of configurable, controllable solvers with:

    -  a common interface
    -  a control handler with: pause, continue, exit, and callback
    -  ease in selecting initial population conditions: guess, random, etc
    -  ease in checkpointing and restarting from a log or saved state
    -  the ability to leverage parallel & distributed computing
    -  the ability to apply a selection of logging and/or verbose monitors
    -  the ability to configure solver-independent termination conditions
    -  the ability to impose custom and user-defined penalties and constraints

To get up and running quickly, ``mystic`` also provides infrastructure to:

    - easily generate a model (several standard test models are included)
    - configure and auto-generate a cost function from a model


Current Release
===============

This version is ``mystic-%(relver)s``.

The latest released version of ``mystic`` is available from:

    https://pypi.org/project/mystic

``mystic`` is distributed under a 3-clause BSD license.

    >>> import mystic
    >>> print (mystic.license())


Development Version 
===================

You can get the latest development version with all the shiny new features at:

    https://github.com/uqfoundation

If you have a new contribution, please submit a pull request.


Installation
============

``mystic`` is packaged to install from source, so you must
download the tarball, unzip, and run the installer::

    [download]
    $ tar -xvzf mystic-%(thisver)s.tar.gz
    $ cd mystic-%(thisver)s
    $ python setup py build
    $ python setup py install

You will be warned of any missing dependencies and/or settings
after you run the "build" step above. ``mystic`` depends on ``dill``, ``numpy``
and ``sympy``, so you should install them first. There are several
functions within ``mystic`` where ``scipy`` is used if it is available;
however, ``scipy`` is an optional dependency. Having ``matplotlib`` installed
is necessary for running several of the examples, and you should
probably go get it even though it's not required. ``matplotlib`` is required
for results visualization available in the scripts packaged with ``mystic``.

Alternately, ``mystic`` can be installed with ``pip`` or ``easy_install``::

    $ pip install mystic


Requirements
============

``mystic`` requires:

    - ``python``, **version >= 2.6** or **version >= 3.1**, or ``pypy``
    - ``numpy``, **version >= 1.0**
    - ``sympy``, **version >= 0.6.7**
    - ``dill``, **version >= 0.2.7.1**
    - ``klepto``, **version >= 0.1.4**

Optional requirements:

    - ``setuptools``, **version >= 0.6**
    - ``matplotlib``, **version >= 0.91**
    - ``scipy``, **version >= 0.6.0**
    - ``pathos``, **version >= 0.2.1**
    - ``pyina``, **version >= 0.2.0.dev0**


More Information
================

Probably the best way to get started is to look at the tests and
examples provided within ``mystic``. See ``mystic.examples`` and ``mystic.tests``
for a set of scripts that demonstrate the configuration and launching of 
optimization jobs for one of the sample models in ``mystic.models``.
Many of the included examples are standard optimization test problems.
The source code is also generally well documented, so further questions
may be resolved by inspecting the code itself.  Please also feel free to
submit a ticket on github, or ask a question on stackoverflow (**@Mike McKerns**).
If you would like to share how you use ``mystic`` in your work, please send an email (to **mmckerns at uqfoundation dot org**).

Instructions on building a new model are in ``mystic.models.abstract_model``.
``mystic`` provides base classes for two types of models:

    - ``AbstractFunction``   [evaluates ``f(x)`` for given evaluation points ``x``]
    - ``AbstractModel``      [generates ``f(x,p)`` for given coefficients ``p``]

``mystic`` also provides some convienence functions to help you build a
model instance and a cost function instance on-the-fly. For more
information, see ``mystic.forward_model``.  It is, however, not necessary
to use base classes or the model builder in building your own model or
cost function, as any standard python function can be used as long as it
meets the basic ``AbstractFunction`` interface of ``cost = f(x)``.

All ``mystic`` solvers are highly configurable, and provide a robust set of
methods to help customize the solver for your particular optimization
problem. For each solver, a minimal (``scipy.optimize``) interface is also
provided for users who prefer to configure and launch their solvers as a
single function call. For more information, see ``mystic.abstract_solver``
for the solver API, and each of the individual solvers for their minimal
functional interface.

``mystic`` enables solvers to use parallel computing whenever the user provides
a replacement for the (serial) python ``map`` function.  ``mystic`` includes a
sample ``map`` in ``mystic.python_map`` that mirrors the behavior of the
built-in python ``map``, and a ``pool`` in ``mystic.pools`` that provides ``map``
functions using the ``pathos`` (i.e. ``multiprocessing``) interface. ``mystic``
solvers are designed to utilize distributed and parallel tools provided by
the ``pathos`` package. For more information, see ``mystic.abstract_map_solver``,
``mystic.abstract_ensemble_solver``, and the ``pathos`` documentation at
http://dev.danse.us/trac/pathos.

Important classes and functions are found here:

    - ``mystic.solvers``                  [solver optimization algorithms]
    - ``mystic.termination``              [solver termination conditions]
    - ``mystic.strategy``                 [solver population mutation strategies]
    - ``mystic.monitors``                 [optimization monitors]
    - ``mystic.symbolic``                 [symbolic math in constaints]
    - ``mystic.constraints``              [constraints functions]
    - ``mystic.penalty``                  [penalty functions]
    - ``mystic.collapse``                 [checks for dimensional collapse]
    - ``mystic.coupler``                  [decorators for function coupling]
    - ``mystic.pools``                    [parallel worker pool interface]
    - ``mystic.munge``                    [file readers and writers]
    - ``mystic.scripts``                  [model and convergence plotting]
    - ``mystic.support``                  [hypercube measure support plotting]
    - ``mystic.forward_model``            [cost function generator]
    - ``mystic.tools``                    [constraints, wrappers, and other tools]
    - ``mystic.cache``                    [results caching and archiving]
    - ``mystic.models``                   [models and test functions]
    - ``mystic.math``                     [mathematical functions and tools]

Important functions within ``mystic.math`` are found here:

    - ``mystic.math.Distribution``        [a sampling distribution object]
    - ``mystic.math.legacydata``          [classes for legacy data observations]
    - ``mystic.math.discrete``            [classes for discrete measures]
    - ``mystic.math.measures``            [tools to support discrete measures]
    - ``mystic.math.approx``              [tools for measuring equality]
    - ``mystic.math.grid``                [tools for generating points on a grid]
    - ``mystic.math.distance``            [tools for measuring distance and norms]
    - ``mystic.math.poly``                [tools for polynomial functions]
    - ``mystic.math.samples``             [tools related to sampling]
    - ``mystic.math.integrate``           [tools related to integration]
    - ``mystic.math.stats``               [tools related to distributions]

Solver and model API definitions are found here:

    - ``mystic.abstract_solver``          [the solver API definition]
    - ``mystic.abstract_map_solver``      [the parallel solver API]
    - ``mystic.abstract_ensemble_solver`` [the ensemble solver API]
    - ``mystic.models.abstract_model``    [the model API definition]

``mystic`` also provides several convience scripts that are used to visualize
models, convergence, and support on the hypercube. These scripts are installed
to a directory on the user's ``$PATH``, and thus can be run from anywhere:

   - ``mystic_log_reader.py``            [parameter and cost convergence]
   - ``mystic_collapse_plotter.py``      [convergence and dimensional collapse]
   - ``mystic_model_plotter.py``         [model surfaces and solver trajectories]
   - ``support_convergence.py``          [convergence plots for measures]
   - ``support_hypercube.py``            [parameter support on the hypercube]
   - ``support_hypercube_measures.py``   [measure support on the hypercube]
   - ``support_hypercube_scenario.py``   [scenario support on the hypercube]

Typing ``--help`` as an argument to any of the above scripts will print out an
instructive help message.


Citation
========

If you use ``mystic`` to do research that leads to publication, we ask that you
acknowledge use of ``mystic`` by citing the following in your publication::

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns, Patrick Hung, and Michael Aivazis,
    "mystic: highly-constrained non-convex optimization and UQ", 2009- ;
    http://trac.mystic.cacr.caltech.edu/project/mystic

Please see http://trac.mystic.cacr.caltech.edu/project/mystic or
http://arxiv.org/pdf/1202.1056 for further information.

""" % {'relver' : stable_version, 'thisver' : this_version}

# write readme file
with open('README', 'w') as file:
    file.write(long_description)

# generate 'info' file contents
def write_info_py(filename='mystic/info.py'):
    contents = """# THIS FILE GENERATED FROM SETUP.PY
this_version = '%(this_version)s'
stable_version = '%(stable_version)s'
readme = '''%(long_description)s'''
license = '''%(license_text)s'''
"""
    with open(filename, 'w') as file:
        file.write(contents % {'this_version' : this_version,
                               'stable_version' : stable_version,
                               'long_description' : long_description,
                               'license_text' : license_text })
    return

# write info file
write_info_py()

# build the 'setup' call
setup_code = """
setup(name='mystic',
      version='%s',
      description='highly-constrained non-convex optimization and uncertainty quantification',
      long_description = '''%s''',
      author = 'Mike McKerns',
      maintainer = 'Mike McKerns',
      license = '3-clause BSD',
      platforms = ['Linux', 'Windows', 'Mac'],
      url = 'https://pypi.org/project/mystic',
      download_url = 'https://github.com/uqfoundation/mystic/releases/download/mystic-%s/mystic-%s.tar.gz',
      classifiers = ('Development Status :: 5 - Production/Stable',
                     'Intended Audience :: Developers',
                     'Intended Audience :: Science/Research',
                     'License :: OSI Approved :: BSD License',
                     'Programming Language :: Python :: 2',
                     'Programming Language :: Python :: 3',
                     'Topic :: Scientific/Engineering',
                     'Topic :: Software Development'),

      packages = ['mystic','mystic.models','mystic.math','mystic.cache'],
      package_dir = {'mystic':'mystic','mystic.models':'models',
                     'mystic.math':'_math','mystic.cache':'cache'},
""" % (target_version, long_description, stable_version, stable_version)

# add dependencies
sysversion = sys.version_info[:2]
if sysversion < (2,6) or (sysversion >= (3,0) and sysversion <= (3,1)):
    numpy_version = '>=1.0, <1.8.0'
    sympy_version = '>=0.6.7, <1.1'
elif sysversion == (2,6) or (sysversion >= (3,2) and sysversion <= (3,3)):
    numpy_version = '>=1.0, <1.12.0'
    sympy_version = '>=0.6.7, <1.1'
else:
    numpy_version = '>=1.0'
    sympy_version = '>=0.6.7'#, <0.7.4'
dill_version = '>=0.2.7.1'
klepto_version = '>=0.1.4'
scipy_version = '>=0.6.0'
matplotlib_version = '>=0.91'
if has_setuptools:
    setup_code += """
      zip_safe=False,
      install_requires = ('numpy%s', 'sympy%s', 'klepto%s', 'dill%s'),
""" % (numpy_version, sympy_version, klepto_version, dill_version)

# add the scripts, and close 'setup' call
setup_code += """
    scripts=['scripts/mystic_log_reader.py',
             'scripts/mystic_model_plotter.py',
             'scripts/mystic_collapse_plotter.py',
             'scripts/support_convergence.py',
             'scripts/support_hypercube.py',
             'scripts/support_hypercube_measures.py',
             'scripts/support_hypercube_scenario.py'])
"""

# exec the 'setup' code
exec(setup_code)

# if dependencies are missing, print a warning
try:
    import numpy
    import sympy
    import klepto
    import dill
    #import scipy
    #import matplotlib #XXX: has issues being zip_safe
except ImportError:
    print("\n***********************************************************")
    print("WARNING: One of the following dependencies is unresolved:")
    print("    numpy %s" % numpy_version)
    print("    sympy %s" % sympy_version)
    print("    klepto %s" % klepto_version)
    print("    dill %s" % dill_version)
    print("    scipy %s (optional)" % scipy_version)
    print("    matplotlib %s (optional)" % matplotlib_version)
    print("***********************************************************\n")


if __name__=='__main__':
    pass

# end of file
