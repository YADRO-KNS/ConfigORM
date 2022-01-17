import shutil
import unittest
import os
from configparser import *

from configorm import *

package_dir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.path.join(package_dir, 'fixtures/config.ini')

connector = IniConnector(connection_string=connection_string)


class BaseSection(Section):
    class Meta:
        connector = connector


class SectionA(BaseSection):
    string_field = StringField()
    integer_field = IntegerField()
    float_field = FloatField()
    bool_field = BooleanField()
    null_value = IntegerField(null=True)
    list_of_int = ListField(var_type=int)
    list_of_str = ListField(var_type=str)
    list_of_float = ListField(var_type=float)
    list_of_bool = ListField(var_type=bool)


class SectionB(BaseSection):
    string_field = StringField(default='Default Placeholder')
    integer_field = IntegerField(default=33)
    float_field = FloatField(default=0.5)
    bool_field = BooleanField(default=False)
    list_of_int = ListField(var_type=int, default=[3, 2, 1])
    list_of_str = ListField(var_type=str, default=['c', 'b', 'a'])
    list_of_float = ListField(var_type=float, default=[3.3, 2.2, 1.1])
    list_of_bool = ListField(var_type=bool, default=[False, True, False])


class TestConfigORMCreation(unittest.TestCase):
    def test_creation(self):
        """
        Check if Section Model was created.
        """
        self.assertIsNotNone(SectionA)


class TestConfigORMFieldsWithCorrectValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseSection.check_config_integrity()

    def test_string_filed(self):
        result = SectionA.string_field
        self.assertEqual(result, 'Test String')

    def test_integer_field(self):
        result = SectionA.integer_field
        self.assertEqual(result, 42)

    def test_float_field(self):
        result = SectionA.float_field
        self.assertEqual(result, 36.6)

    def test_bool_field(self):
        result = SectionA.bool_field
        self.assertTrue(result)

    def test_null_value(self):
        result = SectionA.null_value
        self.assertIsNone(result)

    def test_list_of_int_field(self):
        result = SectionA.list_of_int
        self.assertEqual(result, [1, 2, 3])

    def test_list_of_str_field(self):
        result = SectionA.list_of_str
        self.assertEqual(result, ['a', 'b', 'c'])

    def test_list_of_float_field(self):
        result = SectionA.list_of_float
        self.assertEqual(result, [1.1, 2.2, 3.3])

    def test_list_of_bool_field(self):
        result = SectionA.list_of_bool
        self.assertEqual(result, [True, False, True])


class TestConfigORMSetFieldValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_config = os.path.join(package_dir, 'fixtures/config.ini')
        restore_config = os.path.join(package_dir, 'fixtures/restore.ini')
        shutil.copy(fixture_config, restore_config)
        BaseSection.check_config_integrity()

    @classmethod
    def tearDownClass(cls) -> None:
        fixture_config = os.path.join(package_dir, 'fixtures/config.ini')
        restore_config = os.path.join(package_dir, 'fixtures/restore.ini')
        shutil.copy(restore_config, fixture_config)
        os.remove(restore_config)

    def test_set_string_filed(self):
        value = 'New Test String'
        SectionA.string_field = value
        result = SectionA.string_field
        self.assertEqual(result, value)

    def test_set_integer_field(self):
        value = 55
        SectionA.integer_field = value
        result = SectionA.integer_field
        self.assertEqual(result, value)

    def test_set_float_field(self):
        value = 33.55
        SectionA.float_field = value
        result = SectionA.float_field
        self.assertEqual(result, value)

    def test_set_bool_field(self):
        value = False
        SectionA.bool_field = value
        result = SectionA.bool_field
        self.assertEqual(result, value)

    def test_set_null_value(self):
        value = 23
        SectionA.null_value = value
        result = SectionA.null_value
        self.assertEqual(result, value)

    def test_set_null_value_with_none(self):
        value = None
        SectionA.null_value = value
        result = SectionA.null_value
        self.assertEqual(result, value)

    def test_set_list_of_int_field(self):
        value = [11, 22, 33]
        SectionA.list_of_int = value
        result = SectionA.list_of_int
        self.assertEqual(result, value)

    def test_set_list_of_str_field(self):
        value = ['z', 'x', 'v']
        SectionA.list_of_str = value
        result = SectionA.list_of_str
        self.assertEqual(result, value)

    def test_set_list_of_float_field(self):
        value = [1.1, 2.2, 3.3]
        SectionA.list_of_float = value
        result = SectionA.list_of_float
        self.assertEqual(result, value)

    def test_set_list_of_bool_field(self):
        value = [False, False, False]
        SectionA.list_of_bool = value
        result = SectionA.list_of_bool
        self.assertEqual(result, value)


class TestConfigORMFieldsWithDefaultValues(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        config = ConfigParser(allow_no_value=True)
        with open(SectionB.meta.connector.connection_string, "r") as file:
            config.read_file(file)
        config.remove_section('SectionB')
        with open(SectionB.meta.connector.connection_string, "w") as file:
            config.write(file)

    def test_string_filed(self):
        result = SectionB.string_field
        self.assertEqual(result, 'Default Placeholder')

    def test_integer_field(self):
        result = SectionB.integer_field
        self.assertEqual(result, 33)

    def test_float_field(self):
        result = SectionB.float_field
        self.assertEqual(result, 0.5)

    def test_bool_field(self):
        result = SectionB.bool_field
        self.assertFalse(result)

    def test_list_of_int_field(self):
        result = SectionB.list_of_int
        self.assertEqual(result, [3, 2, 1])

    def test_list_of_str_field(self):
        result = SectionB.list_of_str
        self.assertEqual(result, ['c', 'b', 'a'])

    def test_list_of_float_field(self):
        result = SectionB.list_of_float
        self.assertEqual(result, [3.3, 2.2, 1.1])

    def test_list_of_bool_field(self):
        result = SectionB.list_of_bool
        self.assertEqual(result, [False, True, False])
