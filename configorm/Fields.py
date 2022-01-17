class Field(object):
    def __init__(self, default=None, null: bool = False, env_override: bool = False):
        self.default = default
        self.null = null
        self.env_override = env_override
        self.section = None
        self.name = None
        self.value = None

        self.meta = None

    def __get__(self, instance, owner):
        value = self.get_value()
        if value is None and self.default is not None:
            return self.default
        if value is None and self.null is True:
            return None
        return self.cast_value(value)

    def cast_value(self, value):
        pass

    def get_value(self):
        return self.meta.connector.get_value(
            section_name=self.section.meta.name,
            attr_name=self.name,
            env_override=self.env_override
        )

    def bind(self, section, name, meta):
        self.section = section
        self.name = name
        self.meta = meta


class IntegerField(Field):
    def __init__(self, default: int = None, null: bool = False, env_override: bool = False):
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value):
        return int(value)


class StringField(Field):
    def __init__(self, default: str = None, null: bool = False, env_override: bool = False):
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value):
        return str(value).strip()


class FloatField(Field):
    def __init__(self, default: float = None, null: bool = False, env_override: bool = False):
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value):
        return float(value)


class BooleanField(Field):
    def __init__(self, default: bool = None, null: bool = False, env_override: bool = False):
        super().__init__(default=default, null=null, env_override=env_override)

    def cast_value(self, value: str):
        if value.lower() in ['true', '1']:
            return True
        elif value.lower() in ['false', '0']:
            return False
        else:
            return bool(value)


class ListField(Field):
    def __init__(self, var_type: type, default: list = None, null: bool = False, env_override: bool = False):
        self.type = var_type
        super().__init__(default=default, null=null, env_override=env_override)

        if self.type not in [int, str, float, bool]:
            raise Exception('Unknown base type %s passed into ListField' % str(self.type))

    def cast_value(self, value):
        result = []
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
