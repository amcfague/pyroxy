import ConfigParser
import logging.config
import os.path


log = logging.getLogger(__name__)


class PyroxyConfig(dict):
    """
    Dictionary mixin that pulls config values from a specified config path using
    :meth:`load_config`.
    """

    APP_CONFIG_SECTION = "main"

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
            self['allowed_extensions'] = map(
                str.strip, self['allowed_extensions'].split(','))
        if 'whitelisted_packages' in self:
            self['whitelisted_packages'] = map(
                str.lower, self['whitelisted_packages'].split(','))
