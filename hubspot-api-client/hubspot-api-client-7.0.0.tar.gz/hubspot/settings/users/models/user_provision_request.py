# coding: utf-8

"""
    Users

    Add, manage, and remove users from your account  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.settings.users.configuration import Configuration


class UserProvisionRequest(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {"email": "str", "role_id": "str", "primary_team_id": "str", "secondary_team_ids": "list[str]", "send_welcome_email": "bool"}

    attribute_map = {"email": "email", "role_id": "roleId", "primary_team_id": "primaryTeamId", "secondary_team_ids": "secondaryTeamIds", "send_welcome_email": "sendWelcomeEmail"}

    def __init__(self, email=None, role_id=None, primary_team_id=None, secondary_team_ids=None, send_welcome_email=None, local_vars_configuration=None):  # noqa: E501
        """UserProvisionRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._email = None
        self._role_id = None
        self._primary_team_id = None
        self._secondary_team_ids = None
        self._send_welcome_email = None
        self.discriminator = None

        self.email = email
        if role_id is not None:
            self.role_id = role_id
        if primary_team_id is not None:
            self.primary_team_id = primary_team_id
        if secondary_team_ids is not None:
            self.secondary_team_ids = secondary_team_ids
        self.send_welcome_email = send_welcome_email

    @property
    def email(self):
        """Gets the email of this UserProvisionRequest.  # noqa: E501

        The created user's email  # noqa: E501

        :return: The email of this UserProvisionRequest.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserProvisionRequest.

        The created user's email  # noqa: E501

        :param email: The email of this UserProvisionRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and email is None:  # noqa: E501
            raise ValueError("Invalid value for `email`, must not be `None`")  # noqa: E501

        self._email = email

    @property
    def role_id(self):
        """Gets the role_id of this UserProvisionRequest.  # noqa: E501

        The user's role  # noqa: E501

        :return: The role_id of this UserProvisionRequest.  # noqa: E501
        :rtype: str
        """
        return self._role_id

    @role_id.setter
    def role_id(self, role_id):
        """Sets the role_id of this UserProvisionRequest.

        The user's role  # noqa: E501

        :param role_id: The role_id of this UserProvisionRequest.  # noqa: E501
        :type: str
        """

        self._role_id = role_id

    @property
    def primary_team_id(self):
        """Gets the primary_team_id of this UserProvisionRequest.  # noqa: E501

        The user's primary team  # noqa: E501

        :return: The primary_team_id of this UserProvisionRequest.  # noqa: E501
        :rtype: str
        """
        return self._primary_team_id

    @primary_team_id.setter
    def primary_team_id(self, primary_team_id):
        """Sets the primary_team_id of this UserProvisionRequest.

        The user's primary team  # noqa: E501

        :param primary_team_id: The primary_team_id of this UserProvisionRequest.  # noqa: E501
        :type: str
        """

        self._primary_team_id = primary_team_id

    @property
    def secondary_team_ids(self):
        """Gets the secondary_team_ids of this UserProvisionRequest.  # noqa: E501

        The user's additional teams  # noqa: E501

        :return: The secondary_team_ids of this UserProvisionRequest.  # noqa: E501
        :rtype: list[str]
        """
        return self._secondary_team_ids

    @secondary_team_ids.setter
    def secondary_team_ids(self, secondary_team_ids):
        """Sets the secondary_team_ids of this UserProvisionRequest.

        The user's additional teams  # noqa: E501

        :param secondary_team_ids: The secondary_team_ids of this UserProvisionRequest.  # noqa: E501
        :type: list[str]
        """

        self._secondary_team_ids = secondary_team_ids

    @property
    def send_welcome_email(self):
        """Gets the send_welcome_email of this UserProvisionRequest.  # noqa: E501

        Whether to send a welcome email  # noqa: E501

        :return: The send_welcome_email of this UserProvisionRequest.  # noqa: E501
        :rtype: bool
        """
        return self._send_welcome_email

    @send_welcome_email.setter
    def send_welcome_email(self, send_welcome_email):
        """Sets the send_welcome_email of this UserProvisionRequest.

        Whether to send a welcome email  # noqa: E501

        :param send_welcome_email: The send_welcome_email of this UserProvisionRequest.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and send_welcome_email is None:  # noqa: E501
            raise ValueError("Invalid value for `send_welcome_email`, must not be `None`")  # noqa: E501

        self._send_welcome_email = send_welcome_email

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], "to_dict") else item, value.items()))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, UserProvisionRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserProvisionRequest):
            return True

        return self.to_dict() != other.to_dict()
