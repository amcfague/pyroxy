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

import collections
import ConfigParser
import logging.config
import os.path


log = logging.getLogger(__name__)


class PyroxyConfig(collections.Mapping):
    """
    Dictionary mixin that pulls config values from a specified config path using
    :meth:`load_config`.
    """

    APP_CONFIG_SECTION = "main"
    PACKAGE_SECTION_PREFIX = "package_"

    def __init__(self, *args, **kwargs):
        self._ds = dict(*args, **kwargs)

    def __iter__(self):
        return iter(self._ds)

    def __len__(self):
        return len(self._ds)

    def __getitem__(self, key):
        return self._ds[key]


    def load_config(self, config_path):
        """
        Verifies that the path specified in :data:`config_path` refers to a
        valid path, and populates the dictionary with values from the config.
        This should be a valid config file. See :ref:`configuration narrative
        <configuration>` for valid config values used throughout the
        application.

        :param config_path:
            Path to a valid Python parser.
        """
        if not os.path.exists(config_path):
            raise Exception("Config file `%s` does not exist.", config_path)

        self._load_logging_config(config_path)
        self._load_application_config(config_path)

    def _load_logging_config(self, config_path):
        """
        Loads the :mod:`logging` config from the config file, using the
        :func:`logging.config.fileConfig` loader.
        """
        logging.config.fileConfig(config_path)

    def _load_application_config(self, config_path):
        """
        Loads the application values from the config file, injecting them as
        keys and values.  This handles the `allowed_extensions` and
        `whitelisted_packages` options separately, as these are entered as
        lists and should be treated as such in the application.
        """
        parser = ConfigParser.ConfigParser()
        parser.read(config_path)
        if not parser.has_section(self.APP_CONFIG_SECTION):
            raise Exception("`%s` does not have a `%s` section." % (
                config_path, self.APP_CONFIG_SECTION))

        self.update(parser.items(self.APP_CONFIG_SECTION))

        if 'allowed_extensions' in self:
            log.debug("Converting `allowed_extensions` to list.")
            self._ds['allowed_extensions'] = map(
                str.strip, self._ds['allowed_extensions'].split(','))
        if 'whitelisted_packages' in self:
            self._ds['whitelisted_packages'] = map(
                str.lower, self._ds['whitelisted_packages'].split(','))
