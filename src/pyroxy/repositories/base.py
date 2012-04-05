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
