import os.path

from pyroxy.exceptions import SecurityException
from pyroxy.repositories.base import BaseRepository


class LocalPypiRepository(BaseRepository):

    def __init__(self, base_path):
        """
        :param base_path: An absolute path to the `web` directory.
        """
        self._base_path = os.path.abspath(base_path)

    def open_index(self, package_name):
        simple_index_path = os.path.join(
                self._base_path, "simple", package_name, "index.html")
        return open(simple_index_path, "r")

    def open_static(self, path):
        static_path = os.path.abspath(os.path.join(self._base_path, path))
        if not static_path.startswith(self._base_path):
            raise SecurityException("Security breach!!")
        return open(static_path, "r")
