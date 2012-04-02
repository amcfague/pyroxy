.. _getting_started :

===========================
Getting started with pyroxy
===========================

pyroxy is a relatively simple `WSGI
<http://en.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_ application
defined by :pep:`333`.  At its heart, its just a web service that completely
replicates the interface of PyPI, with some filtering capabilities.

Setting up pyroxy
-----------------

.. note::

    It is highly recommended that a `virtual environment
    <http://www.virtualenv.org>`_ be used for setting up pyroxy, but it is not
    required.

Simply run the following from the pyroxy base directory:

    ~/pyroxy$ python setup.py develop

This will setup a link to the current git directory, as well as installing all
dependencies.

Running pyroxy
--------------

You can start pyroxy by simply running::

    ~/pyroxy$ python run_app.py etc/development.ini

Assuming there were no errors, you should now be able to access
http://localhost:5000/simple and get a nice directory listing, in much the
same format as from PyPI's official simple site.

Using a passenger file (mod_wsgi, unicorn, etc.)
------------------------------------------------

Instead of using the :file:`run_app.py` driver, one can also deploy this using
what is known as a passenger file.

When using this from another WSGI application (i.e., ``mod_wsgi``), the
imported application would be the :data:`~pyroxy.app` variable defined here.  A
typical WSGI passenger file would look like so::

    from pyroxy import app as application, config
    config.load_config("/etc/path/to/config.ini")

In the passenger file, there simply needs to be a variable name `application`
that behaves like a WSGI application, so importing it here is sufficient.

Configuration
-------------

:ref:`See configuration. <configuration>`
