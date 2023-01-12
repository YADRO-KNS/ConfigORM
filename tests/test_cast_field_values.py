import unittest
from unittest.mock import Mock

from configorm import *


class TestIntegerField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = 1
        cls.str_value = '1'

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = IntegerField()

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = IntegerField()

        self.assertEqual(TestSection.field, self.dir_value)


class TestFloatField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = 1.1
        cls.str_value = '1.1'

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = FloatField()

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = FloatField()

        self.assertEqual(TestSection.field, self.dir_value)


class TestBooleanField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = True
        cls.str_value = 'True'

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = BooleanField()

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = BooleanField()

        self.assertEqual(TestSection.field, self.dir_value)


class TestListOfStrField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = ['a', 'b', 'c']
        cls.str_value = "['a', 'b', 'c']"

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = ListField(var_type=str)

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = ListField(var_type=str)

        self.assertEqual(TestSection.field, self.dir_value)


class TestListOfIntField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = [1, 2, 3]
        cls.str_value = "[1, 2, 3]"

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = ListField(var_type=int)

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = ListField(var_type=int)

        self.assertEqual(TestSection.field, self.dir_value)


class TestListOfFloatField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = [1.1, 2.2, 3.3]
        cls.str_value = "[1.1, 2.2, 3.3]"

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = ListField(var_type=float)

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = ListField(var_type=float)

        self.assertEqual(TestSection.field, self.dir_value)


class TestListOfBoolField(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_value = [True, False, True]
        cls.str_value = "[True, False, True]"

    def test_is_str_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.str_value)

        class TestSection(BaseSection):
            field = ListField(var_type=bool)

        self.assertEqual(TestSection.field, self.dir_value)

    def test_is_dir_value(self):
        class BaseSection(Section):
            class Meta:
                connector = Mock()
                connector.get_value = Mock(return_value=self.dir_value)

        class TestSection(BaseSection):
            field = ListField(var_type=bool)

        self.assertEqual(TestSection.field, self.dir_value)
