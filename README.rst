Background
----------

Since the beginning of time (the 90s), `PyPI <http://pypi.python.org/pypi>`_
has stood as the pinnacle of centralized Python packaging.  Everytime an
`easy_install` or a `pip` command is run, PyPI is servicing a request, routing
you to the correct version, architecture, etc., of the package you requested.
Its very flexible--even allowing package authors to host packages both to PyPI
*and* their personal web sites.

...which is all fine and dandy, until these third-party web sites run into
problems.  Infinite loops due to randomly generated URLs names causing DDoS
attacks, slow download speeds, missing files, and downtime, all affect the end
user's experience.  While `pip` seeks to address some of these issues, the
plain and simple fact of the matter is: **PyPI is no longer a reliable
resource.**

``pyroxy`` is a special kind of proxy that sits between your client and
`PyPI <http://pypi.python.org/pypi>`_; with it, you can restrict what packages
are available, as well as what sources to use.  For example, the default
behavior is to choose PyPI hosted packages, direct download links, or generic
URLs (which are then parsed), in that order--if the higher precendence is
available, the more unreliable are omitted.  With the ability to set
whitelisted packages, this means that you can essentially control what your
clients are accessing at any time!

Documentation
-------------

Documentation can be viewed through PyPI, or by building the documentation
yourself using::

    python setup.py develop
    python setup.py build_sphinx

The latest (and previously published) versions of the documentation `are always
available on RTD <http://readthedocs.org/docs/pyroxy/en/v0.1/>`_.

License
-------

pyroxy is covered by the APL 2.0 license.  See LICENSE for all details.
