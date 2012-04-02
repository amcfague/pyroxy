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

    :raises:
        :exc:`ValueError` if the value could not be coerced to a :const:`True`
        or :const:`False` value.
    :returns:
        :const:`True` or :const:`False`, depending on what :data:`val` was
        coerced to.
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


def pred_filter_internal_download_links(package_name, href, title):
    """
    Predicate used to filter internal download links.  Currently, the only
    config value is ``allowed_extensions``.

    :param string package_name:
        Name of the Python package to retrieve and filter the simple page for.
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
    allowed_extensions = config.get_package_config(
            package_name, 'allowed_extensions')
    if allowed_extensions is None:
        return True

    _, _, extension = title.rpartition('.')
    return extension in allowed_extensions


def pred_filter_home_pages(package_name, href, title):
    """
    Predicate used to filter home pages.

    :param string package_name:
        Name of the Python package to retrieve and filter the simple page for.
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


def pred_filter_external_download_links(package_name, href, title):
    """
    Predicate used to filter external download links.  Currently, the only
    config value is ``allowed_extensions``.

    :param string package_name:
        Name of the Python package to retrieve and filter the simple page for.
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
    :raises:
        If the file could not be opened, a 404 exception will be raised.
    :returns:
        An lxml formatted HTML page as a string, containing the final, filtered
        version of the page.
    """
    try:
        fd = open(index_path, "r")
    except IOError:
        log.exception("Could not open %s for filtering.", index_path)
        bottle.abort(404)

    html_tree = lxml.html.parse(fd)
    html_tree = remove_links(html_tree)
    return lxml.html.tostring(html_tree)


def split_links(package_name, elements):
    """
    Parses through a list of elements, and splits them up based on their type.

    :param string package_name:
        Name of the Python package to retrieve and filter the simple page for.
    :param iterable elements:
        iterable containing :class:`lxml.etree.ElementTree.Element`
    :returns:
        Tuple of lists, ``(external_download_links, home_pages,
        internal_download_links, unknown_links)``.
    """
    external_download_links = []
    home_pages = []
    internal_download_links = []
    unknown_links = []

    for element in elements:
        href = element.get("href")
        title = element.text_content()

        if pred_filter_internal_download_links(package_name, href, title):
            internal_download_links.append(element)
        elif pred_filter_home_pages(package_name, href, title):
            home_pages.append(element)
        elif pred_filter_external_download_links(package_name, href, title):
            external_download_links.append(element)
        else:
            unknown_links.append(element)

    return (external_download_links, home_pages, internal_download_links,
            unknown_links)


def build_links_to_remove(external_download_links, home_pages,
        internal_download_links, unknown_links):
    """
    Generates a list of links to remove based on which links are preferred.

    :param list external_download_links:
        list of internal download links
    :param list home_pages:
        list of home pages
    :param list internal_download_links:
        list of internal download links
    :param list unknown_links:
        list of unknown links, or links that do not match either any of the
        previous three.
    :returns:
        list of :class:`lxml.etree.ElementTree.Element` that are safe to be
        removed.
    """
    if internal_download_links:
        to_be_removed = external_download_links + home_pages + unknown_links
    elif external_download_links:
        to_be_removed = home_pages + unknown_links
    elif home_pages:
        to_be_removed = unknown_links
    else:
        to_be_removed = []

    return to_be_removed


def remove_links(package_name, html_tree):
    """
    Filters out links based on the various predicates.  Unfortunately, right
    now, the predicates aren't configurable.

    :param string package_name:
        Name of the Python package to retrieve and filter the simple page for.
    :param html_tree:
        :mod:`lxml.tree` representing the simple page.
    :returns:
        A modified :mod:`lxml.tree` with specific links filtered out.
    """
    (external_download_links, home_pages, internal_download_links,
            unknown_links) = split_links(package_name,
                    html_tree.iterfind(".//a"))
    to_be_removed = build_links_to_remove(external_download_links, home_pages,
        internal_download_links, unknown_links)

    # So that we preserve the funky formatting of the page, lets make sure that
    # we just pull out the tags in place, without disrupting the HTML page
    # itself.
    for element in to_be_removed:
        element.getnext().drop_tree()
        element.drop_tree()

    return html_tree


@app.route("/simple/<package_name>/")
@app.route("/simple/<package_name>/index.html")
def package_list(package_name):
    """
    Controller used to serve up a package listing.

    :param string package_name:
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
