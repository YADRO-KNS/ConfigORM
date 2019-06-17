from .Fields import Field

SECTION_BASE = '_metaclass_helper_'


def with_metaclass(meta, base=object):
    return meta(SECTION_BASE, (base,), {})


class Metadata(object):
    def __init__(self, section, connector=None):
        self.section = section
        self.connector = connector

        self.fields = {}
        self.name = section.__name__.lower()

    def add_field(self, field_name, field):
        if field_name not in self.fields:
            if isinstance(field, Field):
                field.bind(self.section, field_name, self)
                self.fields[field.name] = field


class SectionBase(type):
    inheritable = {'connector'}

    def __new__(mcs, name, bases, attrs):
        if name == SECTION_BASE or bases[0].__name__ == SECTION_BASE:
            return super(SectionBase, mcs).__new__(mcs, name, bases, attrs)

        meta = attrs.pop('Meta', None)
        meta_options = {}

        if meta:
            for key, value in meta.__dict__.items():
                if not key.startswith('_'):
                    meta_options[key] = value

        for base in bases:
            if not hasattr(base, 'meta'):
                continue

            base_meta = base.meta

            for key in base_meta.__dict__:
                if key in mcs.inheritable and key not in meta_options:
                    meta_options[key] = base_meta.__dict__[key]

        new_meta = meta_options.get('model_metadata_class', Metadata)

        mcs = super(SectionBase, mcs).__new__(mcs, name, bases, attrs)
        mcs.meta = new_meta(mcs, **meta_options)

        fields = []
        for key, value in mcs.__dict__.items():
            if isinstance(value, Field):
                fields.append((key, value))

        for name, field in fields:
            mcs.meta.add_field(name, field)

        return mcs


class Section(with_metaclass(SectionBase)):
    def __init__(self, **kwargs):
        pass

    @classmethod
    def check_config_integrity(cls):
        cls.meta.connector.create_config()

        for section in cls.__subclasses__():
            if cls.meta.connector.is_section_exist(section_name=section.__name__) is False:
                cls.meta.connector.add_section(section_name=section.__name__)

            for field_name, field_entry in section.meta.fields.items():
                if cls.meta.connector.is_attr_exist(section_name=section.__name__, attr_name=field_name) is False:
                    cls.meta.connector.add_attr(section_name=section.__name__, attr_name=field_name, value=field_entry.default)
