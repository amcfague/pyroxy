import os
import time

from bottle import template, static_file, redirect
from operator import itemgetter

from pyroxy import app, config


def format_file_entry(base_path, filename):
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
    root_path = config['pypi_packages_path']
    path = os.path.join(root_path, relative_path)

    # If we have a file, just serve it up immediately.
    if not os.path.isdir(path):
        # This will also catch non-existent files, which will automatically
        # return a 404 error.
        return static_file(relative_path, root_path,
                           download=os.path.basename(path))
    # Redirect with a trailing slash
    elif relative_path and not relative_path.endswith('/'):
        moved_location = "/" + os.path.join("packages", relative_path) + "/"
        redirect(moved_location , 301)

    entries = tuple(format_file_entry(path, entry)
                    for entry in sorted(os.listdir(path)))
    packages_base_path = "/".join(("packages", relative_path)).strip("/")

    return template("directory",
                    entries=entries,
                    packages_base_path=packages_base_path,
                    relative_path=relative_path)
