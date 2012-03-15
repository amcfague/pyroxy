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

import logging
import os
import time

from bottle import template, static_file, redirect
from mimetypes import guess_type

from pyroxy import app, config


log = logging.getLogger(__name__)


def format_file_entry(base_path, filename):
    """
    Generate a tuple of metadata based on a filename and path.

    :param base_path:
        The path that contains `filename`.
    :param filename:
        The filename.
    :returns:
        A tuple containing ``(filename, modification date, file size)``.
    """
    absolute_path = os.path.join(base_path, filename)
    stat = os.stat(absolute_path)
    mdate = time.strftime("%d-%b-%Y %H:%M", time.gmtime(stat.st_mtime))
    if os.path.isdir(absolute_path):
        size = "-"
        filename = filename + "/"
    else:
        size = stat.st_size

    return (filename, mdate, size)


@app.route("/<relative_path:path>")
def serve_static_files(relative_path=""):
    """
    Serves up a static file if needed, or a filtered index path.

    :param relative_path:
        The path relative to the base PyPI path.  This includes packages,
        directories, etc..
    :returns:
        Data containing the response to the request.
    """
    root_path = config['pypi_web_path']
    path = os.path.join(root_path, relative_path)

    # If we have a file, just serve it up immediately.
    if not os.path.isdir(path):
        # This will also catch non-existent files, which will automatically
        # return a 404 error.
        log.info("Serving static file: %s", path)
        content_type = guess_type(relative_path)[0] or \
                "application/octet-stream"
        return static_file(relative_path, root_path,
                           download=os.path.basename(path),
                           mimetype=content_type)

    # Redirect with a trailing slash
    if relative_path and not relative_path.endswith('/'):
        moved_location = relative_path + "/"
        log.info("Redirecting with trailing slash to %s", moved_location)
        redirect(moved_location, 301)

    # If we have an index file available in the current directory, serve it.
    index_path = os.path.join(path, "index.html")
    if os.path.exists(index_path):
        relative_index_path = os.path.join(relative_path, "index.html")
        log.info("Serving index for /%s", relative_index_path)
        return static_file(relative_index_path, root_path, download=False)

    entries = tuple(format_file_entry(path, entry)
                    for entry in sorted(os.listdir(path)))

    log.info("Serving directory: %s", path)
    return template("directory",
                    entries=entries,
                    relative_path=relative_path)
