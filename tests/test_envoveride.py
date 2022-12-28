import os
import unittest

from configorm import *

package_dir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.path.join(package_dir, 'fixtures/config.ini')
connector = IniConnector(connection_string=connection_string)


class BaseSection(Section):
    class Meta:
        connector = connector


class SectionA(BaseSection):
    string_field = StringField(env_override=True)
    integer_field = IntegerField(env_override=True)
    float_field = FloatField(env_override=True)
    bool_field = BooleanField(env_override=True)
    null_value = IntegerField(null=True,)
    list_of_int = ListField(var_type=int, env_override=True)
    list_of_str = ListField(var_type=str, env_override=True)
    list_of_float = ListField(var_type=float, env_override=True)
    list_of_bool = ListField(var_type=bool, env_override=True)


class TestConfigORMFieldsWithEnvVars(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        BaseSection.check_config_integrity()

    def test_string_filed_no_env(self):
        key = 'SECTIONA_STRING_FIELD'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.string_field
        self.assertEqual(result, 'Test String')

    def test_string_filed_env(self):
        env_value = 'Test String Env'
        os.environ['SECTIONA_STRING_FIELD'] = env_value
        result = SectionA.string_field
        self.assertEqual(result, env_value)

    def test_integer_field_no_env(self):
        key = 'SECTIONA_INTEGER_FIELD'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.integer_field
        self.assertEqual(result, 42)

    def test_integer_field_env(self):
        env_value = 43
        os.environ['SECTIONA_INTEGER_FIELD'] = str(env_value)
        result = SectionA.integer_field
        self.assertEqual(result, env_value)

    def test_float_field_no_env(self):
        key = 'SECTIONA_FLOAT_FIELD'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.float_field
        self.assertEqual(result, 36.6)

    def test_float_field_env(self):
        env_value = 1.2
        os.environ['SECTIONA_FLOAT_FIELD'] = str(env_value)
        result = SectionA.float_field
        self.assertEqual(result, env_value)

    def test_bool_field_no_env(self):
        key = 'SECTIONA_BOOL_FIELD'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.bool_field
        self.assertTrue(result)

    def test_bool_field_env(self):
        env_value = 0
        os.environ['SECTIONA_BOOL_FIELD'] = str(env_value)
        result = SectionA.bool_field
        self.assertFalse(result)

    def test_list_of_int_field_no_env(self):
        key = 'SECTIONA_LIST_OF_INT'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.list_of_int
        self.assertEqual(result, [1, 2, 3])

    def test_list_of_int_field_env(self):
        env_value = [4, 5, 6]
        os.environ['SECTIONA_LIST_OF_INT'] = str(env_value)
        result = SectionA.list_of_int
        self.assertEqual(result, env_value)

    def test_list_of_str_field_no_env(self):
        key = 'SECTIONA_LIST_OF_STR'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.list_of_str
        self.assertEqual(result, ['a', 'b', 'c'])

    def test_list_of_str_field_env(self):
        env_value = ['d', 'e', 'f']
        os.environ['SECTIONA_LIST_OF_STR'] = str(env_value)
        result = SectionA.list_of_str
        self.assertEqual(result, env_value)

    def test_list_of_float_field_no_env(self):
        key = 'SECTIONA_LIST_OF_FLOAT'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.list_of_float
        self.assertEqual(result, [1.1, 2.2, 3.3])

    def test_list_of_float_field_env(self):
        env_value = [4.4, 5.5, 6.6]
        os.environ['SECTIONA_LIST_OF_FLOAT'] = str(env_value)
        result = SectionA.list_of_float
        self.assertEqual(result, env_value)

    def test_list_of_bool_field_no_env(self):
        key = 'SECTIONA_LIST_OF_BOOL'
        if key in os.environ:
            os.environ.pop(key)
        result = SectionA.list_of_bool
        self.assertEqual(result, [True, False, True])

    def test_list_of_bool_field_env(self):
        env_value = [False, True, False]
        os.environ['SECTIONA_LIST_OF_BOOL'] = str(env_value)
        result = SectionA.list_of_bool
        self.assertEqual(result, env_value)
