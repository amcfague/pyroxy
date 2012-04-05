import urllib2

from pyroxy.repositories.base import BaseRepository


DEFAULT_PYPI_URL = "http://pypi.python.org"


def urljoin(*segments):
    return "/".join(segments)


class RemotePypiRepository(BaseRepository):

    def __init__(self, pypi_base_url=DEFAULT_PYPI_URL):
        """
        :param pypi_base_url: An absolute URL to the `web` directory online.
        """
        self._url = pypi_base_url

    def open_index(self, package_name):
        """
        See :meth:`pyroxy.repositories.base.BaseRepository.open_index`.
        """
        # Add a trailing slash to indicate the directory; PyPI sometimes hides
        # its index files.
        simple_index_path = urljoin(self._url, "simple", package_name) + "/"
        return urllib2.urlopen(simple_index_path)

    def open_static(self, path):
        """
        See :meth:`pyroxy.repositories.base.BaseRepository.open_static`.
        """
        static_path = urljoin(self._url, path)
        return urllib2.urlopen(static_path)
