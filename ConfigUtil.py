import configparser
import os


class ConfigUtility(object):
    __slots__ = ['_config', 'root_dir', 'config_file', '_env']

    def __init__(self):
        self._config = configparser.RawConfigParser()
        self.root_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(self.root_dir, "main_config.properties")
        self._config.read(self.config_file)
        self._env = str(self._config.get("ENV", "environment"))


class EnvironmentConfig(ConfigUtility):
    __slots__ = ['config_file_path']

    def __init__(self):
        super().__init__()
        self.config_file_path = os.path.join(self.root_dir, self._env)
        self._config.read(self.config_file_path)

    def root_output_path(self):
        return self._config.get("DATA", "root_output_path")


class AppConfig(ConfigUtility):
    __slots__ = ['config_file_path']

    def __init__(self):
        super().__init__()
        self.config_file_path = os.path.join(self.root_dir, "app.properties")
        self._config.read(self.config_file_path)

    ''' QDA QUERIES'''

    def get_info(self):
        return self._config.get("DATA", "info")

   
