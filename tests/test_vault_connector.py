import unittest
from unittest.mock import patch, PropertyMock, Mock

from hvac.exceptions import InvalidPath

from configorm import VaultConnector
from configorm.Connectors import Connector


class TestVaultConnector(unittest.TestCase):
    """
    Base class for "Connection" tests
    """

    def setUp(self) -> None:
        """Set up test."""
        self.mount_point = 'TEST/'
        self.url = 'http://some/url'
        self.token = 'some_token'
        with patch('configorm.Connectors.hvac') as self.mock_hvac, \
                patch('configorm.Connectors.os') as self.mock_os:
            self.connector = VaultConnector(mount_point=self.mount_point, url=self.url, token=self.token)


class TestAttrs(TestVaultConnector):

    def test_subclass_of_connector_class(self):
        ### Assertions ###

        self.assertIs(VaultConnector.__base__, Connector)

    def test_instance_attrs(self):
        """
        Test whether the instance of the "VaultConnector" class
        has the necessary instance attributes.
        """
        ### Assertions ###

        self.assertIs(self.connector.mount_point, self.mount_point)

        self.assertEqual(
            self.connector._client,
            self.mock_hvac.Client(
                url=self.url,
                token=self.token
            )
        )


class TestVaultApi(TestVaultConnector):
    def test_method(self):
        ### Run and Assertions ###

        self.assertEqual(self.connector._client.secrets.kv.v2, self.connector._vault_api)


class TestIsConfigExist(TestVaultConnector):
    def test_method(self):
        ### Run and Assertions ###

        self.assertTrue(self.connector.is_config_exist())


class TestCreateConfig(TestVaultConnector):
    def test_method(self):
        ### Run and Assertions ###

        self.assertIsNone(self.connector.create_config())


@patch('configorm.Connectors.os')
@patch('configorm.Connectors.VaultConnector._vault_api', new_callable=PropertyMock)
class TestGetValue(TestVaultConnector):

    def test_get_value_no_override(self, mock__vault_api, mock_os):
        ### Setup ###

        data = 'some_data'
        attr_name = 'attr_name'
        response = {
            'data': {
                'data': {
                    attr_name.upper(): data
                }
            }
        }
        mock__vault_api.return_value.read_secret.return_value = response

        section_name = 'section'

        ### Run ###

        result = self.connector.get_value(section_name=section_name, attr_name=attr_name)

        ### Assertions ###

        self.assertEqual(result, data)
        mock__vault_api.return_value.read_secret.assert_called_once_with(
            path='SECTION',
            mount_point=self.mount_point
        )

    def test_get_value_override(self, mock__vault_api, mock_os):
        ### Setup ###

        data = 'some_data'
        attr_name = 'attr_name'
        section_name = 'section'
        mock_os.getenv.return_value = data

        ### Run ###

        result = self.connector.get_value(section_name=section_name, attr_name=attr_name, env_override=True)

        ### Assertions ###

        self.assertEqual(result, data)
        mock__vault_api.assert_not_called()
        mock_os.getenv.assert_called_once_with('SECTION_ATTR_NAME')


@patch('configorm.Connectors.VaultConnector._vault_api', new_callable=PropertyMock)
class TestIsSectionExist(TestVaultConnector):

    def test_is_section_exist_success(self, mock__vault_api):
        ### Setup ###

        section_name = 'section_name'

        ### Run ###

        result = self.connector.is_section_exist(section_name=section_name)

        ### Assertions ###

        self.assertTrue(result)
        mock__vault_api.return_value.read_secret.assert_called_once_with(
            path='SECTION_NAME',
            mount_point=self.mount_point
        )

    def test_is_section_exist_failure(self, mock__vault_api):
        ### Setup ###

        section_name = 'section_name'
        mock__vault_api.return_value.read_secret.side_effect = InvalidPath

        ### Run ###

        result = self.connector.is_section_exist(section_name=section_name)

        ### Assertions ###

        self.assertFalse(result)
        mock__vault_api.return_value.read_secret.assert_called_once_with(
            path='SECTION_NAME',
            mount_point=self.mount_point
        )


@patch('configorm.Connectors.VaultConnector._vault_api', new_callable=PropertyMock)
class TestIsAttrExist(TestVaultConnector):

    def test_is_attr_exist_success(self, mock__vault_api):
        ### Setup ###

        data = 'some_data'
        attr_name = 'attr_name'
        response = {
            'data': {
                'data': {
                    attr_name.upper(): data
                }
            }
        }

        section_name = 'section_name'
        mock__vault_api.return_value.read_secret.return_value = response

        ### Run ###

        result = self.connector.is_attr_exist(section_name=section_name, attr_name=attr_name)

        ### Assertions ###

        self.assertTrue(result)
        mock__vault_api.return_value.read_secret.assert_called_once_with(
            path='SECTION_NAME',
            mount_point=self.mount_point
        )

    def test_is_attr_exist_failure(self, mock__vault_api):
        ### Setup ###

        section_name = 'section_name'
        attr_name = 'attr_name'

        mock__vault_api.return_value.read_secret.side_effect = InvalidPath

        ### Run ###

        result = self.connector.is_attr_exist(section_name=section_name, attr_name=attr_name)

        ### Assertions ###

        self.assertFalse(result)


class TestAddSection(TestVaultConnector):
    def test_method(self):
        ### Run and Assertions ###

        section_name = 'section_name'

        self.assertIsNone(self.connector.add_section(section_name=section_name))


@patch('configorm.Connectors.VaultConnector._vault_api', new_callable=PropertyMock)
class TestAddAttr(TestVaultConnector):

    def test_attr_update(self, mock__vault_api):
        ### Setup ###

        section_name = 'section_name'
        attr_name = 'attr_name'
        value = 'value'

        self.connector.is_section_exist = Mock(return_value=True)

        ### Run ###

        self.connector.add_attr(section_name=section_name, attr_name=attr_name, value=value)

        ### Assertions ###

        mock__vault_api.return_value.patch.assert_called_once_with(
            path='SECTION_NAME',
            mount_point=self.mount_point,
            secret={'ATTR_NAME': value}
        )

        self.connector.is_section_exist.assert_called_once_with(section_name)

    def test_attr_create(self, mock__vault_api):
        ### Setup ###

        section_name = 'section_name'
        attr_name = 'attr_name'
        value = 'value'

        self.connector.is_section_exist = Mock(return_value=False)

        ### Run ###

        self.connector.add_attr(section_name=section_name, attr_name=attr_name, value=value)

        ### Assertions ###

        mock__vault_api.return_value.create_or_update_secret.assert_called_once_with(
            path='SECTION_NAME',
            mount_point=self.mount_point,
            secret={'ATTR_NAME': value}
        )

        self.connector.is_section_exist.assert_called_once_with(section_name)
