.. _configuration:

=============
Configuration
=============

All configuration options should be made under the ``[main]`` section.

--------
Required
--------

The following are essential to operation, and do NOT provide defaults.

.. glossary::

    pypi_web_path
        Path to the PyPI web directory; in the PyPI directory hierarchy, this
        is typically the directory called :file:`web`.

--------
Optional
--------

.. glossary::
    :sorted:

    allowed_extensions
        Comma separated list of allowed extensions.  If this is not set, all
        extensions will be permitted.  Defaults to ``None``.

    always_show_external_links
        If :const:`True`, will always show external links, even if they would
        normally be filtered out.  Defaults to :const:`False`.

    always_show_home_pages
        If :const:`True`, will always show home pages, even if they would
        normally be filtered out.  Defaults to :const:`False`.

    pypi_packages_path
        Path to the PyPI packages directory.  Defaults to
        :file:`{pypi_web_path}/packages`.

    pypi_simple_path
        Path to the PyPI simple directory.  Defaults to
        :file:`{pypi_web_path}/simple`.

-------
Logging
-------

All logging config is handled using the :mod:`logging` module.  The full
documentation of how to configured a logging file based config can be
referenced from :ref:`the official documentation <logging-config-fileformat>`.
