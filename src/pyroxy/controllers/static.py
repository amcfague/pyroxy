import logging
import os
import time

from bottle import template, static_file, redirect

from pyroxy import app, config


log = logging.getLogger()


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
    root_path = config['pypi_web_path']
    path = os.path.join(root_path, relative_path)

    # If we have a file, just serve it up immediately.
    if not os.path.isdir(path):
        # This will also catch non-existent files, which will automatically
        # return a 404 error.
        log.info("Serving static file: %s", path)
        return static_file(relative_path, root_path,
                           download=os.path.basename(path))
    # Redirect with a trailing slash
    elif relative_path and not relative_path.endswith('/'):
        moved_location = relative_path + "/"
        log.info("Redirecting with trailing slash to %s", moved_location)
        redirect(moved_location , 301)

    entries = tuple(format_file_entry(path, entry)
                    for entry in sorted(os.listdir(path)))

    log.info("Serving directory: %s", path)
    return template("directory",
                    entries=entries,
                    relative_path=relative_path)
