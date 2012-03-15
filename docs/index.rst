.. _index:

==================================
Welcome to pyroxy's documentation!
==================================

Since the beginning of time (the 90s), `PyPI <http://pypi.python.org/pypi>`_
has stood as the pinnacle of centralized Python packaging.  Everytime an
:program:`easy_install` or a :program:`pip` command is run, PyPI is servicing a
request, routing you to the correct version, architecture, etc., of the package
you requested.  Its very flexible--even allowing package authors to host
packages both to PyPI *and* their personal web sites.

...which is all fine and dandy, until these third-party web sites run into
problems.  Infinite loops due to randomly generated URLs names causing DDoS
attacks, slow download speeds, missing files, and downtime, all affect the end
user's experience.  While :program:`pip` seeks to address some of these issues,
the plain and simple fact of the matter is: **PyPI is no longer a reliable
resource.**

:mod:`pyroxy` is a special kind of proxy that sits between your client and
`PyPI <http://pypi.python.org/pypi>`_; with it, you can restrict what packages
are available, as well as what sources to use.  For example, the default
behavior is to choose PyPI hosted packages, direct download links, or generic
URLs (which are then parsed), in that order--if the higher precendence is
available, the more unreliable are omitted.  With the ability to set
whitelisted packages, this means that you can essentially control what your
clients are accessing at any time!

.. warning::

    Currently, :mod:`pyroxy` only supports locally available PyPI
    repositories, which means you'll need to have a mirror of PyPI, ala
    :pep:`381`.  This will definitely change in the future.

-----------------------
Narrative Documentation
-----------------------

.. toctree::
    :maxdepth: 1
    :glob:

    narr/getting_started
    narr/configuration
    narr/troubleshooting

-------------
API Reference
-------------

.. toctree::
    :maxdepth: 1
    :glob:

    api/*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

