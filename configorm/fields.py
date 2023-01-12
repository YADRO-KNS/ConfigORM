import typing


class Field:
    """Field prototype class"""

    def __init__(self,
                 default: typing.Optional[typing.Any] = None,
                 null: bool = False,
                 env_override: bool = False
                 ) -> None:
        self.default = default
        self.null = null
        self.env_override = env_override
        self.section: typing.Optional[typing.Any] = None
        self.name: typing.Optional[typing.Any] = None
        self.value: typing.Optional[typing.Any] = None

        self.meta: typing.Optional[typing.Any] = None

    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        value = self.meta.connector.get_value(
            section_name=self.section.meta.name,
            attr_name=self.name,
            env_override=self.env_override
        )
        if value is None and self.default is not None:
            return self.default
        if value is None and self.null is True:
            return None
        return self.cast_value(value) if self.check_value(value) is False else value

    def __set__(self, instance: typing.Any, value: str) -> None:
        if value is None:
            if self.null is False:
                raise ValueError('None value passed into non null Field')
            else:
                self.meta.connector.set_value(section_name=self.section.meta.name, attr_name=self.name, value=value)
        elif self.check_value(value) is True:
            self.meta.connector.set_value(section_name=self.section.meta.name, attr_name=self.name, value=value)
        else:
            raise TypeError('Incorrect type passed into Field')

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        pass

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        pass

    def bind(self, section: typing.Any, name: typing.Any, meta: typing.Any) -> None:
        """Binds field instance to Section"""
        self.section = section
        self.name = name
        self.meta = meta


class IntegerField(Field):
    """Field class for integer values"""

    def __init__(self, default: int = None, null: bool = False, env_override: bool = False) -> None:
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        return int(value)

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        return isinstance(value, int)


class StringField(Field):
    """Field class for string values"""

    def __init__(self, default: str = None, null: bool = False, env_override: bool = False) -> None:
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        return str(value).strip()

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        return isinstance(value, str)


class FloatField(Field):
    """Field class for float values"""

    def __init__(self, default: float = None, null: bool = False, env_override: bool = False) -> None:
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        return float(value)

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        return isinstance(value, float)


class BooleanField(Field):
    """Field class for boolean values"""

    def __init__(self, default: bool = None, null: bool = False, env_override: bool = False) -> None:
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        if value.lower() in ['true', '1']:
            return True
        elif value.lower() in ['false', '0']:
            return False
        else:
            return bool(value)

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        return isinstance(value, bool)


class ListField(Field):
    """Field class for list of values"""

    def __init__(self, var_type: type, default: list = None, null: bool = False, env_override: bool = False) -> None:
        self.type = var_type
        super().__init__(default=default, null=null, env_override=env_override)

        if self.type not in [int, str, float, bool]:
            raise Exception('Unknown base type %s passed into ListField' % str(self.type))

    def cast_value(self, value: str) -> typing.Any:
        """
        Cast value to the field type
        :param value: value to cast
        :return: processed value
        """
        result: typing.List[typing.Any] = []
        for element in value.replace('[', '').replace(']', '').split(','):
            if self.type == int:
                result.append(int(element.strip()))
            elif self.type == str:
                result.append(element.strip().replace("'", ''))
            elif self.type == float:
                result.append(float(element.strip()))
            elif self.type == bool:
                if element.strip().lower() in ['true', '1']:
                    result.append(True)
                elif element.strip().lower() in ['false', '0']:
                    result.append(False)
                else:
                    result.append(bool(element.strip()))
        return result

    def check_value(self, value: typing.Any) -> bool:
        """
        Check if value type is the same as field type
        :param value: value to check
        :return: check result
        """
        return isinstance(value, list) and all(isinstance(n, self.type) for n in value)
