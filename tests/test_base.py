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
    string = StringField()
    integer = IntegerField()
    float = FloatField()
    bool = BooleanField()
    null_value = IntegerField(null=True)


class SectionB(BaseSection):
    string = StringField(default='Default Placeholder')
    integer = IntegerField(default=33)
    float = FloatField(default=0.5)
    bool = BooleanField(default=False)


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
        result = SectionA.string
        self.assertEqual(result, 'Test String')

    def test_integer_field(self):
        result = SectionA.integer
        self.assertEqual(result, 42)

    def test_float_field(self):
        result = SectionA.float
        self.assertEqual(result, 36.6)

    def test_bool_field(self):
        result = SectionA.bool
        self.assertTrue(result)

    def test_null_value(self):
        result = SectionA.null_value
        self.assertIsNone(result)


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
        result = SectionB.string
        self.assertEqual(result, 'Default Placeholder')

    def test_integer_field(self):
        result = SectionB.integer
        self.assertEqual(result, 33)

    def test_float_field(self):
        result = SectionB.float
        self.assertEqual(result, 0.5)

    def test_bool_field(self):
        result = SectionB.bool
        self.assertFalse(result)

