import os.path
from mock import patch, sentinel
from pyroxy.controllers.static import format_file_entry
from pyroxy.tests import PyroxyTestCase


class TestStaticController(PyroxyTestCase):

    @patch("time.strftime")
    @patch("time.gmtime")
    @patch("os.stat")
    @patch("os.path.isdir")
    def test_format_file_entry_directory(self, mock_isdir, mock_stat,
            mock_gmtime, mock_strftime):
        base_path = "/some/path"
        filename = "madness.txt"

        mock_isdir.return_value = True
        mock_stat().st_mtime = sentinel.st_mtime
        mock_stat().st_size = sentinel.st_size
        mock_strftime.return_value = sentinel.mdate

        ret = format_file_entry(base_path, filename)

        # Because stat will be called for plenty of other things, this cannot
        # check for the call count--only that it was called at least once with
        # the correct arguments.
        mock_stat.assert_called_with(os.path.join(base_path, filename))
        self.assertEquals(ret, (filename + "/", sentinel.mdate, "-"))

    @patch("time.strftime")
    @patch("time.gmtime")
    @patch("os.stat")
    @patch("os.path.isdir")
    def test_format_file_entry_file(self, mock_isdir, mock_stat,
            mock_gmtime, mock_strftime):
        base_path = "/some/path"
        filename = "madness.txt"

        mock_isdir.return_value = False
        mock_stat().st_mtime = sentinel.st_mtime
        mock_stat().st_size = sentinel.st_size
        mock_strftime.return_value = sentinel.mdate

        ret = format_file_entry(base_path, filename)

        # Because stat will be called for plenty of other things, this cannot
        # check for the call count--only that it was called at least once with
        # the correct arguments.
        mock_stat.assert_called_with(os.path.join(base_path, filename))
        self.assertEquals(ret, (filename, sentinel.mdate, sentinel.st_size))
