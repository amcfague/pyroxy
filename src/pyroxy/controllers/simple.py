import logging
import os.path

import bottle
import lxml.html

from pyroxy import app, config


log = logging.getLogger(__name__)


def pred_filter_internal_download_links(href, title):
    allowed_extensions = config.get('allowed_extensions')
    if allowed_extensions is None:
        return True

    _, _, extension = title.rpartition('.')
    return extension in allowed_extensions


def pred_filter_home_pages(href, title):
    return href.startswith("http") and "home_page" in title


def pred_filter_external_download_links(href, title):
    return "download_url" in title


def filter_index(index_path):
    try:
        fd = open(index_path, "r")
    except IOError:
        log.exception("Could not open simple index for filtering.")
        bottle.abort(404)

    html_tree = lxml.html.parse(fd)
    html_tree = remove_links(html_tree)
    return lxml.html.tostring(html_tree)


def remove_links(html_tree):
    external_download_links = []
    home_pages = []
    internal_download_links = []
    unknown_links = []

    for element in html_tree.iterfind(".//a"):
        href = element.get("href")
        title = element.text_content()

        if pred_filter_internal_download_links(href, title):
            internal_download_links.append(element)
        elif pred_filter_home_pages(href, title):
            home_pages.append(element)
        elif pred_filter_external_download_links(href, title):
            external_download_links.append(element)
        else:
            log.warning("Unknown link %s (%s)", title, href)
            unknown_links.append(element)

    if internal_download_links:
        log.debug("Internal download links used.")
        to_be_removed = external_download_links + home_pages + unknown_links
    elif external_download_links:
        log.debug("External download links used.")
        to_be_removed = home_pages + unknown_links
    elif home_pages:
        to_be_removed = unknown_links
    else:
        log.debug("Home pages used.")
        to_be_removed = []

    for element in to_be_removed:
        log.debug("Filtering %s", title)
        element.getnext().drop_tree()
        element.drop_tree()

    return html_tree


@app.route("/simple/<package_name>/")
@app.route("/simple/<package_name>/index.html")
def package_list(package_name):
    package_index_path = os.path.join(
        config['pypi_web_path'], "simple", package_name, "index.html")
    return filter_index(package_index_path)
