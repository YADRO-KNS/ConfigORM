from configparser import ConfigParser


class Connector(object):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def get_value(self, section_name: str, attr_name: str):
        pass


class IniConnector(Connector):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def get_value(self, section_name: str, attr_name: str):
        config = ConfigParser()
        config.read(self.connection_string)

        result = None
        for section in config.sections():
            if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                for attr in config[section]:
                    if attr.lower().replace(' ', '_') == attr_name.lower().replace(' ', '_'):
                        result = config[section][attr]

        return result
