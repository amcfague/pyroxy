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


import pyroxy.controllers.packages
import pyroxy.controllers.simple
