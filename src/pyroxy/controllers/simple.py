import logging
import os.path

import bottle
import lxml.html

from pyroxy import app, config


log = logging.getLogger(__name__)


def pred_filter_package(href, name):
    return True


def pred_filter_index(href, title):
    allowed_extensions = config.get('allowed_extensions')
    if allowed_extensions is None:
        return True

    _, _, extension = title.rpartition('.')
    return extension in allowed_extensions


def filter_index(index_path, predicate):
    log.info("Filtering simple index at %s", index_path)

    try:
        fd = open(index_path, "r")
    except IOError:
        log.exception("Could not open simple index for filtering.")
        bottle.abort(404)

    html_tree = lxml.html.parse(fd)
    html_tree = remove_links(html_tree, predicate)
    return lxml.html.tostring(html_tree)


def remove_links(html_tree, pred):
    for element in html_tree.iterfind(".//a"):
        href = element.get("href")
        title = element.text_content()

        if not pred(href, title):
            log.debug("Filtering %s", title)
            element.getnext().drop_tree()
            element.drop_tree()
    
    return html_tree


@app.route("/simple")
@app.route("/simple/<package_name>")
def redirect_simple_list(package_name=None):
    if package_name:
        url = "/simple/%s/"
    else:
        url = "/simple/"
    
    log.info("Redirecting with trailing slash to %s", url)
    bottle.redirect(url, 301)


@app.route("/simple/")
def simple_list():
    index_path = os.path.join(
        config['pypi_web_path'], "simple", "index.html")
    return filter_index(index_path, pred_filter_package)


@app.route("/simple/<package_name>/")
def package_list(package_name):
    package_index_path = os.path.join(
        config['pypi_web_path'], "simple", package_name, "index.html")
    return filter_index(package_index_path, pred_filter_index)
