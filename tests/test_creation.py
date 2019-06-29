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
    string_field = StringField(default='Default Placeholder', null=False)
    integer_field = IntegerField(default=33, null=False)
    float_field = FloatField(default=0.5, null=False)
    bool_field = BooleanField(default=False, null=False)
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
        self.assertEqual(config['SectionA']['string_field'], SectionA.string_field)

    def test_config_integer_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(int(config['SectionA']['integer_field']), SectionA.integer_field)

    def test_config_float_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(float(config['SectionA']['float_field']), SectionA.float_field)

    def test_config_bool_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['bool_field'], str(SectionA.bool_field))

    def test_config_list_of_int_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['list_of_int'], str(SectionA.list_of_int))

    def test_config_list_of_str_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['list_of_str'], str(SectionA.list_of_str))

    def test_config_list_of_float_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['list_of_float'], str(SectionA.list_of_float))

    def test_config_list_of_bool_value(self):
        config = ConfigParser()
        config.read(SectionA.meta.connector.connection_string)
        self.assertEqual(config['SectionA']['list_of_bool'], str(SectionA.list_of_bool))
