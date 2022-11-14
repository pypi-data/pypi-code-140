# coding: utf-8

"""
    DevCycle Bucketing API

    Documents the DevCycle Bucketing API which provides and API interface to User Bucketing and for generated SDKs.  # noqa: E501

    OpenAPI spec version: 1.0.0

    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401
import sys
import os

import six

import devcycle_python_sdk

class UserData(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'user_id': 'str',
        'email': 'str',
        'name': 'str',
        'language': 'str',
        'country': 'str',
        'app_version': 'str',
        'app_build': 'str',
        'custom_data': 'object',
        'private_custom_data': 'object',
        'created_date': 'float',
        'last_seen_date': 'float',
        'platform': 'str',
        'platform_version': 'str',
        'device_model': 'str',
        'sdk_type': 'str',
        'sdk_version': 'str'
    }

    attribute_map = {
        'user_id': 'user_id',
        'email': 'email',
        'name': 'name',
        'language': 'language',
        'country': 'country',
        'app_version': 'appVersion',
        'app_build': 'appBuild',
        'custom_data': 'customData',
        'private_custom_data': 'privateCustomData',
        'created_date': 'createdDate',
        'last_seen_date': 'lastSeenDate',
        'platform': 'platform',
        'platform_version': 'platformVersion',
        'device_model': 'deviceModel',
        'sdk_type': 'sdkType',
        'sdk_version': 'sdkVersion'
    }

    def __init__(self, user_id=None, email=None, name=None, language=None, country=None, app_version=None, app_build=None, custom_data=None, private_custom_data=None, created_date=None, last_seen_date=None, device_model=None):  # noqa: E501
        """UserData - a model defined in Swagger"""  # noqa: E501

        self._user_id = None
        self._email = None
        self._name = None
        self._language = None
        self._country = None
        self._app_version = None
        self._app_build = None
        self._custom_data = None
        self._private_custom_data = None
        self._created_date = None
        self._last_seen_date = None
        self._platform = 'Python'
        version_file = open(os.path.join(os.path.dirname(devcycle_python_sdk.__file__), 'VERSION.txt'))
        VERSION = version_file.read().strip()
        self._platform_version = sys.version[:5]
        self._device_model = None
        self._sdk_type = 'server'
        self._sdk_version = VERSION
        self.discriminator = None
        self.user_id = user_id

        if email is not None:
            self.email = email
        if name is not None:
            self.name = name
        if language is not None:
            self.language = language
        if country is not None:
            self.country = country
        if app_version is not None:
            self.app_version = app_version
        if app_build is not None:
            self.app_build = app_build
        if custom_data is not None:
            self.custom_data = custom_data
        if private_custom_data is not None:
            self.private_custom_data = private_custom_data
        if created_date is not None:
            self.created_date = created_date
        if last_seen_date is not None:
            self.last_seen_date = last_seen_date
        if device_model is not None:
            self.device_model = device_model

    @property
    def user_id(self):
        """Gets the user_id of this UserData.  # noqa: E501

        Unique id to identify the user  # noqa: E501

        :return: The user_id of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        """Sets the user_id of this UserData.

        Unique id to identify the user  # noqa: E501

        :param user_id: The user_id of this UserData.  # noqa: E501
        :type: str
        """
        if user_id is None:
            raise ValueError("Invalid value for `user_id`, must not be `None`")  # noqa: E501

        self._user_id = user_id

    @property
    def email(self):
        """Gets the email of this UserData.  # noqa: E501

        User's email used to identify the user on the dashboard / target audiences  # noqa: E501

        :return: The email of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserData.

        User's email used to identify the user on the dashboard / target audiences  # noqa: E501

        :param email: The email of this UserData.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def name(self):
        """Gets the name of this UserData.  # noqa: E501

        User's name used to identify the user on the dashboard / target audiences  # noqa: E501

        :return: The name of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UserData.

        User's name used to identify the user on the dashboard / target audiences  # noqa: E501

        :param name: The name of this UserData.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def language(self):
        """Gets the language of this UserData.  # noqa: E501

        User's language in ISO 639-1 format  # noqa: E501

        :return: The language of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._language

    @language.setter
    def language(self, language):
        """Sets the language of this UserData.

        User's language in ISO 639-1 format  # noqa: E501

        :param language: The language of this UserData.  # noqa: E501
        :type: str
        """

        self._language = language

    @property
    def country(self):
        """Gets the country of this UserData.  # noqa: E501

        User's country in ISO 3166 alpha-2 format  # noqa: E501

        :return: The country of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, country):
        """Sets the country of this UserData.

        User's country in ISO 3166 alpha-2 format  # noqa: E501

        :param country: The country of this UserData.  # noqa: E501
        :type: str
        """

        self._country = country

    @property
    def app_version(self):
        """Gets the app_version of this UserData.  # noqa: E501

        App Version of the running application  # noqa: E501

        :return: The app_version of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._app_version

    @app_version.setter
    def app_version(self, app_version):
        """Sets the app_version of this UserData.

        App Version of the running application  # noqa: E501

        :param app_version: The app_version of this UserData.  # noqa: E501
        :type: str
        """

        self._app_version = app_version

    @property
    def app_build(self):
        """Gets the app_build of this UserData.  # noqa: E501

        App Build number of the running application  # noqa: E501

        :return: The app_build of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._app_build

    @app_build.setter
    def app_build(self, app_build):
        """Sets the app_build of this UserData.

        App Build number of the running application  # noqa: E501

        :param app_build: The app_build of this UserData.  # noqa: E501
        :type: str
        """

        self._app_build = app_build

    @property
    def custom_data(self):
        """Gets the custom_data of this UserData.  # noqa: E501

        User's custom data to target the user with, data will be logged to DevCycle for use in dashboard.  # noqa: E501

        :return: The custom_data of this UserData.  # noqa: E501
        :rtype: object
        """
        return self._custom_data

    @custom_data.setter
    def custom_data(self, custom_data):
        """Sets the custom_data of this UserData.

        User's custom data to target the user with, data will be logged to DevCycle for use in dashboard.  # noqa: E501

        :param custom_data: The custom_data of this UserData.  # noqa: E501
        :type: object
        """

        self._custom_data = custom_data

    @property
    def private_custom_data(self):
        """Gets the private_custom_data of this UserData.  # noqa: E501

        User's custom data to target the user with, data will not be logged to DevCycle only used for feature bucketing.  # noqa: E501

        :return: The private_custom_data of this UserData.  # noqa: E501
        :rtype: object
        """
        return self._private_custom_data

    @private_custom_data.setter
    def private_custom_data(self, private_custom_data):
        """Sets the private_custom_data of this UserData.

        User's custom data to target the user with, data will not be logged to DevCycle only used for feature bucketing.  # noqa: E501

        :param private_custom_data: The private_custom_data of this UserData.  # noqa: E501
        :type: object
        """

        self._private_custom_data = private_custom_data

    @property
    def created_date(self):
        """Gets the created_date of this UserData.  # noqa: E501

        Date the user was created, Unix epoch timestamp format  # noqa: E501

        :return: The created_date of this UserData.  # noqa: E501
        :rtype: float
        """
        return self._created_date

    @created_date.setter
    def created_date(self, created_date):
        """Sets the created_date of this UserData.

        Date the user was created, Unix epoch timestamp format  # noqa: E501

        :param created_date: The created_date of this UserData.  # noqa: E501
        :type: float
        """

        self._created_date = created_date

    @property
    def last_seen_date(self):
        """Gets the last_seen_date of this UserData.  # noqa: E501

        Date the user was created, Unix epoch timestamp format  # noqa: E501

        :return: The last_seen_date of this UserData.  # noqa: E501
        :rtype: float
        """
        return self._last_seen_date

    @last_seen_date.setter
    def last_seen_date(self, last_seen_date):
        """Sets the last_seen_date of this UserData.

        Date the user was created, Unix epoch timestamp format  # noqa: E501

        :param last_seen_date: The last_seen_date of this UserData.  # noqa: E501
        :type: float
        """

        self._last_seen_date = last_seen_date

    @property
    def platform(self):
        """Gets the platform of this UserData.  # noqa: E501

        Platform the Client SDK is running on  # noqa: E501

        :return: The platform of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """Sets the platform of this UserData.

        Platform the Client SDK is running on  # noqa: E501

        :param platform: The platform of this UserData.  # noqa: E501
        :type: str
        """

        self._platform = platform

    @property
    def platform_version(self):
        """Gets the platform_version of this UserData.  # noqa: E501

        Version of the platform the Client SDK is running on  # noqa: E501

        :return: The platform_version of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._platform_version

    @platform_version.setter
    def platform_version(self, platform_version):
        """Sets the platform_version of this UserData.

        Version of the platform the Client SDK is running on  # noqa: E501

        :param platform_version: The platform_version of this UserData.  # noqa: E501
        :type: str
        """

        self._platform_version = platform_version

    @property
    def device_model(self):
        """Gets the device_model of this UserData.  # noqa: E501

        User's device model  # noqa: E501

        :return: The device_model of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._device_model

    @device_model.setter
    def device_model(self, device_model):
        """Sets the device_model of this UserData.

        User's device model  # noqa: E501

        :param device_model: The device_model of this UserData.  # noqa: E501
        :type: str
        """

        self._device_model = device_model

    @property
    def sdk_type(self):
        """Gets the sdk_type of this UserData.  # noqa: E501

        DevCycle SDK type  # noqa: E501

        :return: The sdk_type of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._sdk_type

    @sdk_type.setter
    def sdk_type(self, sdk_type):
        """Sets the sdk_type of this UserData.

        DevCycle SDK type  # noqa: E501

        :param sdk_type: The sdk_type of this UserData.  # noqa: E501
        :type: str
        """
        allowed_values = ["api", "server"]  # noqa: E501
        if sdk_type not in allowed_values:
            raise ValueError(
                "Invalid value for `sdk_type` ({0}), must be one of {1}"  # noqa: E501
                .format(sdk_type, allowed_values)
            )

        self._sdk_type = sdk_type

    @property
    def sdk_version(self):
        """Gets the sdk_version of this UserData.  # noqa: E501

        DevCycle SDK Version  # noqa: E501

        :return: The sdk_version of this UserData.  # noqa: E501
        :rtype: str
        """
        return self._sdk_version

    @sdk_version.setter
    def sdk_version(self, sdk_version):
        """Sets the sdk_version of this UserData.

        DevCycle SDK Version  # noqa: E501

        :param sdk_version: The sdk_version of this UserData.  # noqa: E501
        :type: str
        """

        self._sdk_version = sdk_version

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(UserData, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UserData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
