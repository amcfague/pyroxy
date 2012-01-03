import os
import time

from bottle import template, static_file, redirect

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


@app.route("/packages")
@app.route("/packages/")
@app.route("/packages/<relative_path:path>")
def serve_packages(relative_path=""):
    # Redirect with a trailing slash
    if relative_path and not relative_path.endswith('/'):
        redirect("/" + os.path.join("packages", relative_path) + "/"), 301

    root_path = config['pypi_packages_path']
    path = os.path.join(root_path, relative_path)

    if not os.path.isdir(path):
        return static_file(relative_path, root_path,
                           download=os.path.basename(path))

    entries = tuple(format_file_entry(path, entry) for entry in os.listdir(path))
    packages_base_path = "/".join(("packages", relative_path)).strip("/")

    return template("directory",
                    entries=entries,
                    packages_base_path=packages_base_path,
                    relative_path=relative_path)
