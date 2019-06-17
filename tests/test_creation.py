import unittest
import os
from configparser import *
from configorm import *

package_dir = os.path.abspath(os.path.dirname(__file__))
connection_string = os.path.join(package_dir, 'test.ini')
connector = IniConnector(connection_string=connection_string)


class BaseSection(Section):
    class Meta:
        connector = connector


class SectionA(BaseSection):
    string = StringField(default='Default Placeholder', null=False)
    integer = IntegerField(default=33, null=False)
    float = FloatField(default=0.5, null=False)
    bool = BooleanField(default=False, null=False)


class TestConfigORMCreation(unittest.TestCase):
    def test_creation(self):
        """
        Check if Section Model was created.
        """

        self.assertIsNotNone(SectionA)


class TestConfigORMRecreated(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        BaseSection.check_config_integrity()

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(SectionA.meta.connector.connection_string)

    def test_new_config_content(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertIn('SectionA', config.sections())

    def test_config_string_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['string'], SectionA.string)

    def test_config_integer_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(int(config['SectionA']['integer']), SectionA.integer)

    def test_config_float_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(float(config['SectionA']['float']), SectionA.float)

    def test_config_bool_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['bool'], str(SectionA.bool))
