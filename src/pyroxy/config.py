import ConfigParser
import logging.config
import os.path


log = logging.getLogger(__name__)


class PyroxyConfig(dict):

    APP_CONFIG_SECTION = "main"

    def load_config(self, config_path):
        if not os.path.exists(config_path):
            raise Exception("Config file `%s` does not exist.", config_path)

        self._load_logging_config(config_path)
        self._load_application_config(config_path)

    def _load_logging_config(self, config_path):
        logging.config.fileConfig(config_path)

    def _load_application_config(self, config_path):
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
