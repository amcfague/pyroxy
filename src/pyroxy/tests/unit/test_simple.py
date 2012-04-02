from bottle import HTTPError
from mock import Mock, patch, sentinel

from pyroxy.controllers.simple import (
        asbool, pred_filter_internal_download_links, pred_filter_home_pages,
        pred_filter_external_download_links, filter_index, package_list)
from pyroxy.tests import PyroxyTestCase


class TestSimpleController(PyroxyTestCase):

    @patch("__builtin__.bool")
    def test_asbool_not_string(self, mock_bool):
        mock_bool.return_value = sentinel.val
        for val in ({}, (), 0, None):
            self.assertEqual(asbool(val), sentinel.val)
            mock_bool.assert_called_once_with(val)
            mock_bool.reset_mock()

    @patch("__builtin__.bool")
    def test_asbool_true(self, mock_bool):
        for val in ("TRuE", "YES", "y", "1"):
            self.assertTrue(asbool(val))
            self.assertFalse(mock_bool.called)

    @patch("__builtin__.bool")
    def test_asbool_false(self, mock_bool):
        for val in ("FALse", "NO", "n", "0"):
            self.assertFalse(asbool(val))
            self.assertFalse(mock_bool.called)

    @patch("__builtin__.bool")
    def test_asbool_invalid(self, mock_bool):
        for val in ("nottrue", "ZOMG", "5", ""):
            self.assertRaises(ValueError, asbool, val)

    @patch("pyroxy.controllers.simple.config")
    def test_pred_filter_internal_download_links(self, mock_config):
        mock_config.get_package_config.return_value = ('txt',)
        title = "test.nottxt"

        ret = pred_filter_internal_download_links(
                sentinel.package_name, sentinel.href, title)

        self.assertFalse(ret)

    @patch("pyroxy.controllers.simple.config")
    def test_pred_filter_internal_download_links_no_ext(self, mock_config):
        mock_config.get_package_config.return_value = None
        mock_title = Mock()

        ret = pred_filter_internal_download_links(
                sentinel.package_name, sentinel.href, mock_title)

        self.assertTrue(ret)
        self.assertFalse(mock_title.rpartition.called)

    def test_pred_filter_home_pages(self):
        self.assertTrue(pred_filter_home_pages(
            sentinel.package_name, "http://...", "home_page"))
        self.assertFalse(pred_filter_home_pages(
            sentinel.package_name, "http://...", "not_home"))
        self.assertFalse(pred_filter_home_pages(
            sentinel.package_name, "../", "home_page"))

    def test_pred_filter_external_download_links(self):
        self.assertTrue(pred_filter_external_download_links(
            sentinel.package_name, sentinel.href, "download_url"))
        self.assertFalse(pred_filter_external_download_links(
            sentinel.package_name, sentinel.href, "notdownload"))

    @patch("pyroxy.controllers.simple.remove_links")
    @patch("lxml.html")
    @patch("__builtin__.open")
    def test_filter_index(self, mock_open, mock_html, mock_remove_links):
        mock_open.return_value = sentinel.fd
        mock_html.parse.return_value = sentinel.html_tree
        mock_remove_links.return_value = sentinel.html_tree
        mock_html.tostring.return_value = sentinel.html_str

        ret = filter_index(sentinel.index_path)

        mock_open.assert_called_once_with(sentinel.index_path, "r")
        mock_html.parse.assert_called_once_with(sentinel.fd)
        mock_remove_links.assert_called_once_with(sentinel.html_tree)
        mock_html.tostring.assert_called_once_with(sentinel.html_tree)
        self.assertEquals(ret, sentinel.html_str)

    @patch("__builtin__.open")
    def test_filter_index_failure(self, mock_open):
        mock_open.side_effect = IOError()
        self.assertRaises(HTTPError, filter_index, sentinel.index_path)

    @patch("pyroxy.controllers.simple.filter_index")
    @patch.dict("pyroxy.controllers.simple.config._ds")
    def test_package_list_non_whitelisted(self, mock_filter_index):
        from pyroxy.controllers.simple import config

        package_name = "pylons"
        base_path = "/base/path"

        config._ds['pypi_web_path'] = base_path
        config._ds['whitelisted_packages'] = ()
        mock_filter_index.return_value = sentinel.filter_index

        ret = package_list(package_name)

        self.assertEquals(ret, sentinel.filter_index)

    @patch("pyroxy.controllers.simple.static_file")
    @patch.dict("pyroxy.controllers.simple.config._ds")
    def test_package_list_whitelisted(self, mock_static_file):
        from pyroxy.controllers.simple import config

        package_name = "pylons"
        base_path = "/base/path"

        config._ds['pypi_web_path'] = base_path
        config._ds['whitelisted_packages'] = (package_name,)
        mock_static_file.return_value = sentinel.static_file

        ret = package_list(package_name)

        mock_static_file.assert_called_once_with("index.html",
                root="%s/simple/%s" % (base_path, package_name))
        self.assertEquals(ret, sentinel.static_file)
