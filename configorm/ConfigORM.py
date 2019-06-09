from .Fields import Field

SECTION_BASE = '_metaclass_helper_'


def with_metaclass(meta, base=object):
    return meta(SECTION_BASE, (base,), {})


class Metadata(object):
    def __init__(self, section, connector=None, **kwargs):
        self.section = section
        self.connector = connector

        self.fields = {}

        self.name = section.__name__.lower()

        for key, value in kwargs.items():
            setattr(self, key, value)

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
        for key in kwargs:
            setattr(self, key, kwargs[key])
