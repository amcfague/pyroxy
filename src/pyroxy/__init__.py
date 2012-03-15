"""
This drives the running and setup of :mod:`bottle`, including setting up a
template path, setting up :class:`pyroxy.config.PyroxyConfig`, and creating a
WSGI application, :data:`pyroxy.app`.

When using this from another WSGI application (i.e., :prog:`mod_wsgi`), the
imported application would be the :data:`~pyroxy.app` variable defined here.
I.e., a typical WSGI passenger file would look like so::

    from pyroxy import app as application, config
    config.load_config("/etc/path/to/config.ini")

In the passenger file, there simply needs to be a variable name `application`
that behaves like a WSGI application, so importing it here is sufficient.
"""
import bottle
import os.path
import pkg_resources

from pyroxy.config import PyroxyConfig


__all__ = ['app', 'config']


app = bottle.Bottle()
config = PyroxyConfig()

# Add the custom location of the views path!
views_path = os.path.join(
    pkg_resources.resource_filename("pyroxy", ""), "views")
bottle.TEMPLATE_PATH = [views_path]


import pyroxy.controllers.simple
import pyroxy.controllers.static
