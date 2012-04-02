import unittest
import webtest

import pyroxy


class PyroxyTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(PyroxyTestCase, self).__init__(*args, **kwargs)

        self.app = webtest.TestApp(pyroxy.app)
