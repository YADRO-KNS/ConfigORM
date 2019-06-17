from configparser import ConfigParser
from abc import ABC, abstractmethod
import os


class Connector(ABC):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    @abstractmethod
    def is_config_exist(self) -> bool:
        pass

    @abstractmethod
    def create_config(self) -> None:
        pass

    @abstractmethod
    def get_value(self, section_name: str, attr_name: str):
        pass

    @abstractmethod
    def is_section_exist(self, section_name: str) -> bool:
        pass

    @abstractmethod
    def is_attr_exist(self, section_name: str, attr_name: str) -> bool:
        pass

    @abstractmethod
    def add_section(self, section_name: str):
        pass

    @abstractmethod
    def add_attr(self, section_name: str, attr_name: str, value: str):
        pass


class IniConnector(Connector):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def get_value(self, section_name: str, attr_name: str):
        config = ConfigParser(allow_no_value=True)
        config.read(self.connection_string)

        result = None
        for section in config.sections():
            if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                for attr in config[section]:
                    if attr.lower().replace(' ', '_') == attr_name.lower().replace(' ', '_'):
                        result = config[section][attr]

        return result

    def is_section_exist(self, section_name: str) -> bool:
        config = ConfigParser(allow_no_value=True)
        config.read(self.connection_string)

        result = False
        for section in config.sections():
            if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                result = True

        return result

    def is_attr_exist(self, section_name: str, attr_name: str) -> bool:
        config = ConfigParser(allow_no_value=True)
        config.read(self.connection_string)

        result = False
        for section in config.sections():
            if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                for attr in config[section]:
                    if attr.lower().replace(' ', '_') == attr_name.lower().replace(' ', '_'):
                        result = True

        return result

    def add_section(self, section_name: str):
        if self.is_section_exist(section_name=section_name) is False:
            config = ConfigParser(allow_no_value=True)
            config.read(self.connection_string)
            config.add_section(section=(section_name.replace('_', ' ')))
            with open(file=self.connection_string, mode='w') as file:
                config.write(fp=file)

    def add_attr(self, section_name: str, attr_name: str, value: str):
        if self.is_attr_exist(section_name=section_name, attr_name=attr_name) is False:
            if value is not None:
                value = str(value)
            config = ConfigParser(allow_no_value=True)
            config.read(self.connection_string)
            config.set(section=section_name, option=attr_name, value=value)
            with open(file=self.connection_string, mode='w') as file:
                config.write(fp=file)

    def is_config_exist(self) -> bool:
        return os.path.isfile(self.connection_string)

    def create_config(self) -> None:
        if self.is_config_exist() is False:
            file = open(file=self.connection_string, mode="w+")
            file.close()
