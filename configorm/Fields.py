class Field(object):
    def __init__(self, default=None, null: bool = False):
        self.default = default
        self.null = null
        self.section = None
        self.name = None
        self.value = None

        self.meta = None

    def __get__(self, instance, owner):
        value = self.get_value()
        if value is None and self.default is not None:
            value = self.default
        if value is None and self.null is True:
            return None
        return self.cast_value(value)

    def cast_value(self, value):
        pass

    def get_value(self):
        return self.meta.connector.get_value(section_name=self.section.meta.name, attr_name=self.name)

    def bind(self, section, name, meta):
        self.section = section
        self.name = name
        self.meta = meta


class IntegerField(Field):
    def __init__(self, default: int = None, null: bool = False):
        super().__init__(default=default, null=null)

    def cast_value(self, value):
        return int(value)


class StringField(Field):
    def __init__(self, default: str = None, null: bool = False):
        super().__init__(default=default, null=null)

    def cast_value(self, value):
        return str(value).strip()


class FloatField(Field):
    def __init__(self, default: float = None, null: bool = False):
        super().__init__(default=default, null=null)

    def cast_value(self, value):
        return float(value)


class BooleanField(Field):
    def __init__(self, default: bool = None, null: bool = False):
        super().__init__(default=default, null=null)

    def cast_value(self, value):
        if value == 'True':
            return True
        elif value == 'False':
            return False
        else:
            return bool(value)
