import os
import csv

from devassistant import settings

class ConfigManager(object):
    """
    Stores all configuration values which should be preserved across multiple
    launches of devassistant GUI.
    It provides saving and loading configuration values from a file.
    """

    def __init__(self):
        self.config_dict = dict()
        self.config_file = settings.CONFIG_FILE
        self.config_changed = False

    def load_configuration_file(self):
        """Load all configuration from file
        """
        if not os.path.exists(self.config_file):
            return
        with open(self.config_file,'r') as file:
            csvreader = csv.reader(file, delimiter='=', escapechar='\\', quoting=csv.QUOTE_NONE)
            for line in csvreader:
                if len(line) == 2:
                    key, value = line
                    self.config_dict[key] = value

    def save_configuration_file(self):
        """Save all configuration into file
        Only if config file does not yet exist or configuration was changed
        """
        if os.path.exists(self.config_file) and not self.config_changed:
            return
        dirname = os.path.dirname(self.config_file)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.config_file,'w') as file:
            csvwriter = csv.writer(file, delimiter='=', escapechar='\\', quoting=csv.QUOTE_NONE)
            for key, value in self.config_dict.items():
                csvwriter.writerow([key, value])
        self.config_changed = False

    def get_config_value(self, name):
        """Get configuration value for given name.
        """
        return self.config_dict.get(name)

    def set_config_value(self, name, value):
        """Set configuration value with given name.
        Value can be string or boolean type.
        """
        if value == True:
            value = "True"
        elif value == False:
            if name in self.config_dict:
                del self.config_dict[name]
                self.config_changed = True
            return
        if not name in self.config_dict or self.config_dict[name] != value:
            self.config_changed = True
            self.config_dict[name] = value

config_manager = ConfigManager()
