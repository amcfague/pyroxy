# Copyright 2011 Andrew McFague
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This drives the running and setup of :mod:`bottle`, including setting up a
template path, setting up :class:`pyroxy.config.PyroxyConfig`, and creating a
WSGI application, :data:`pyroxy.app`.
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
