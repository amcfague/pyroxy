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
`http://localhost:5000/simple`_ and get a nice directory listing, in much the
same format as from PyPI's official simple site.

Configuration
-------------

:ref:`See configuration. <configuration>`
