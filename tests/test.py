import unittest
import os

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
    def test_string_filed(self):
        self.assertEqual(SectionA.string, 'Test String')

    def test_integer_field(self):
        self.assertEqual(SectionA.integer, 42)

    def test_float_field(self):
        self.assertEqual(SectionA.float, 36.6)

    def test_bool_field(self):
        self.assertTrue(SectionA.bool)


class TestConfigORMFieldsWithDefaultValues(unittest.TestCase):
    def test_string_filed(self):
        self.assertEqual(SectionB.string, 'Default Placeholder')

    def test_integer_field(self):
        self.assertEqual(SectionB.integer, 33)

    def test_float_field(self):
        self.assertEqual(SectionB.float, 0.5)

    def test_bool_field(self):
        self.assertFalse(SectionB.bool)
