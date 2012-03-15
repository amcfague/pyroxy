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
import os.path

import bottle
import lxml.html

from bottle import static_file
from pyroxy import app, config


log = logging.getLogger(__name__)


def asbool(val):
    """
    Attempts to coerce :data:`val` to a boolean value.  This is largely based
    off of :func:`paste.deploy.converters.asbool` with a few stylistic tweaks
    added.

    Raises a :exc:`ValueError` if the specified value cannot be coerced to a
    True or False value.
    """
    # If its not a string or string-like object, just do our best.
    if not isinstance(val, basestring):
        return bool(val)

    obj = val.strip().lower()
    if obj in ['true', 'yes', 'on', 'y', 't', '1']:
        return True
    elif obj in ['false', 'no', 'off', 'n', 'f', '0']:
        return False
    else:
        raise ValueError("Could not coerce `%s` to True/False" % obj)


def pred_filter_internal_download_links(href, title):
    """
    Predicate used to filter internal download links.  Currently, the only
    config value is ``allowed_extensions``.

    :param href:
        Relative URL generated from the simple page (i.e.,
        `../../packages/a/b/c/pyroxy-0.1.tar.gz`)
    :param title:
        Text component of the link from the simple page.  This can include
        suffixes such as `download_url` and `home_page`, which can be used as
        part of the filter.
    :return:
        :const:`True` if the internal download link should be included in the
        output, :const:`False` otherwise.
    """
    allowed_extensions = config.get('allowed_extensions')
    if allowed_extensions is None:
        return True

    _, _, extension = title.rpartition('.')
    return extension in allowed_extensions


def pred_filter_home_pages(href, title):
    """
    Predicate used to filter home pages.

    :param href:
        Absolute URL to a `home page` (i.e., a third party site)
    :param title:
        Text component of the link from the simple page.  This can include
        suffixes such as `download_url` and `home_page`, which can be used as
        part of the filter.
    :returns:
        :const:`True` if the home page link should be included in the output,
        :const:`False` otherwise.
    """
    return href.startswith("http") and "home_page" in title


def pred_filter_external_download_links(href, title):
    """
    Predicate used to filter external download links.  Currently, the only
    config value is ``allowed_extensions``.

    :param href:
        Absolute URL pointing to a downloadable file on a third-party web site.
    :param title:
        Text component of the link from the simple page.  This can include
        suffixes such as `download_url` and `home_page`, which can be used as
        part of the filter.
    :returns:
        :const:`True` if the external download link should be included in the
        output, :const:`False` otherwise.
    """
    return "download_url" in title


def filter_index(index_path):
    """
    Path to an index page (index.html, typically).  This function will parse the
    results into an lxml tree, call :func:`remove_links` on the resulting tree,
    and then convert it back to an HTML page.

    :param index_path:
        Absolute path to the index file.  This MUST already be created, and must
        be a file.
    :returns:
        An lxml formatted HTML page as a string, containing the final, filtered
        version of the page.  If the file could not be opened, a 404 exception
        will be raised.
    """
    try:
        fd = open(index_path, "r")
    except IOError:
        log.exception("Could not open simple index for filtering.")
        bottle.abort(404)

    html_tree = lxml.html.parse(fd)
    html_tree = remove_links(html_tree)
    return lxml.html.tostring(html_tree)


def remove_links(html_tree):
    """
    Filters out links based on the various predicates.  Unfortunately, right
    now, the predicates aren't configurable.

    :param html_tree:
        :mod:`lxml.tree` representing the simple page.

    Returns a modified :mod:`lxml.tree` with specific links filtered out.
    """
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
            log.debug("Filtering out link: %s (%s)", title, href)
            unknown_links.append(element)

    if internal_download_links:
        log.debug("Internal download links used.")
        if asbool(config.get('always_include_external', True)):
            to_be_removed = home_pages + unknown_links
        else:
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
    """
    Controller used to serve up a package listing.

    :param package_name:
        Name of the Python package to retrieve and filter the simple page for.
        Capitalization matters, depending on your operating system--i.e., on
        Linux, `pylons` != `Pylons`.
    :returns:
        The raw simple page if the package was whitelisted, or a filtered page
        if it was not.
    """
    package_index_path = os.path.join(
        config['pypi_web_path'], "simple", package_name, "index.html")
    if package_name.lower() in config.get('whitelisted_packages', []):
        root = os.path.join(config['pypi_web_path'], "simple", package_name)
        return static_file("index.html", root=root)
    else:
        return filter_index(package_index_path)
