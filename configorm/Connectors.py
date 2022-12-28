import os
import typing
from abc import ABC, abstractmethod
from configparser import ConfigParser

import hvac
from hvac.api.vault_api_base import VaultApiBase
from hvac.exceptions import InvalidPath


class Connector(ABC):

    @abstractmethod
    def is_config_exist(self) -> bool:
        pass

    @abstractmethod
    def create_config(self) -> None:
        pass

    @abstractmethod
    def get_value(self, section_name: str, attr_name: str, env_override: bool = False):
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
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def get_value(self, section_name: str, attr_name: str, env_override: bool = False):
        config = ConfigParser(allow_no_value=True)
        config.read(self.connection_string)
        result = None

        if env_override is True:
            result = os.getenv(f'{section_name}_{attr_name}'.upper())

        if result is None:
            for section in config.sections():
                if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                    for attr in config[section]:
                        if attr.lower().replace(' ', '_') == attr_name.lower().replace(' ', '_'):
                            result = config[section][attr]

        return result

    def set_value(self, section_name: str, attr_name: str, value: str):
        config = ConfigParser(allow_no_value=True)
        if value is not None:
            value = str(value)
        if self.is_section_exist(section_name=section_name) is True:
            if self.is_attr_exist(section_name=section_name, attr_name=attr_name) is True:
                config.read(self.connection_string)
                for section in config.sections():
                    if section.lower().replace(' ', '_') == section_name.lower().replace(' ', '_'):
                        for attr in config[section]:
                            if attr.lower().replace(' ', '_') == attr_name.lower().replace(' ', '_'):
                                config.set(section=section, option=attr, value=value)
                                with open(file=self.connection_string, mode='w') as file:
                                    config.write(fp=file)
            else:
                self.add_attr(section_name=section_name, attr_name=attr_name, value=value)

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


class VaultConnector(Connector):
    def __init__(self, mount_point: str, url: str, token: str):
        self.mount_point = mount_point
        self.url = url
        self.token = token

        self._client = hvac.Client(url=self.url, token=self.token)

    @property
    def _vault_api(self) -> VaultApiBase:
        return self._client.secrets.kv.v2

    def is_config_exist(self) -> bool:
        return True

    def create_config(self) -> None:
        pass

    def get_value(self, section_name: str, attr_name: str, env_override: bool = False) -> typing.Optional[str]:
        key = f'{section_name}_{attr_name}'.upper()
        result: typing.Optional[str] = None
        if env_override:
            result = os.getenv(key)
        if result is None:
            response = self._vault_api.read_secret(path=section_name.upper(), mount_point=self.mount_point)
            result = response["data"]["data"].get(attr_name.upper())
        return result

    def is_section_exist(self, section_name: str) -> bool:
        success = False
        try:
            self._vault_api.read_secret(path=section_name.upper(), mount_point=self.mount_point)
            success = True
        except InvalidPath:
            pass
        return success

    def is_attr_exist(self, section_name: str, attr_name: str) -> bool:
        success = False
        try:
            response = self._vault_api.read_secret(path=section_name.upper(), mount_point=self.mount_point)
            keys = list(response["data"]["data"].keys())
            success = attr_name.upper() in keys
        except InvalidPath:
            pass
        return success

    def add_section(self, section_name: str):
        pass

    def add_attr(self, section_name: str, attr_name: str, value: str):
        if self.is_section_exist(section_name):
            self._vault_api.patch(
                path=section_name.upper(),
                mount_point=self.mount_point,
                secret={
                    attr_name.upper(): value
                }
            )
        else:
            self._vault_api.create_or_update_secret(
                path=section_name.upper(),
                mount_point=self.mount_point,
                secret={
                    attr_name.upper(): value
                }
            )
