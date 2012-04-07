import os.path

import urllib2

from pyroxy.exceptions import SecurityException


__all__ = ["BaseRepository", "LocalPypiRepository", "RemotePypiRepository"]


DEFAULT_PYPI_URL = "http://pypi.python.org"


def urljoin(*segments):
    return "/".join(segments)


class BaseRepository(object):

    def get_index(self, package_name):
        return self.open_index(package_name).read()

    def get_static(self, path):
        return self.open_static(path).read()

    def open_index(self, package_name):
        """
        Opens an index page, based on the specified ``package_name``.  This
        usually resolves to some kind of index.html page.

        :param string package_name:
            The name of the package to resolve.  Depending on the system, this
            may or may not be case sensitive.
        :returns:
            File-like object that implements the :func:`read` method.
        """
        raise NotImplementedError

    def open_static(self, path):
        """
        Opens a static file based on ``path``.

        :param path:
            Relative path to a static file, most likely a binary file.
        :returns:
            File-like object that implements the :func:`read` method.

        warning::

            Be warned, this could be a relatively path that is a parent of the
            root directory.  This function should insure that files outside of
            the root directory cannot be accessed.
        """
        raise NotImplementedError


class LocalPypiRepository(BaseRepository):

    def __init__(self, base_path):
        """
        :param base_path: An absolute path to the `web` directory.
        """
        self._base_path = os.path.abspath(base_path)

    def open_index(self, package_name):
        """
        See :meth:`pyroxy.repositories.BaseRepository.open_index`.
        """
        simple_index_path = os.path.join(
                self._base_path, "simple", package_name, "index.html")
        return open(simple_index_path, "r")

    def open_static(self, path):
        """
        See :meth:`pyroxy.repositories.BaseRepository.open_static`.
        """
        static_path = os.path.abspath(os.path.join(self._base_path, path))
        if not static_path.startswith(self._base_path):
            raise SecurityException("Security breach!!")
        return open(static_path, "r")


class RemotePypiRepository(BaseRepository):

    def __init__(self, pypi_base_url=DEFAULT_PYPI_URL):
        """
        :param pypi_base_url: An absolute URL to the `web` directory online.
        """
        self._url = pypi_base_url

    def open_index(self, package_name):
        """
        See :meth:`pyroxy.repositories.BaseRepository.open_index`.
        """
        # Add a trailing slash to indicate the directory; PyPI sometimes hides
        # its index files.
        simple_index_path = urljoin(self._url, "simple", package_name) + "/"
        return urllib2.urlopen(simple_index_path)

    def open_static(self, path):
        """
        See :meth:`pyroxy.repositories.BaseRepository.open_static`.
        """
        static_path = urljoin(self._url, path)
        return urllib2.urlopen(static_path)
