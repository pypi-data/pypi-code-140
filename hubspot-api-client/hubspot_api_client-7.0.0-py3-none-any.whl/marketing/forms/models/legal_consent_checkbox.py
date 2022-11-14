# coding: utf-8

"""
    FormsExternalService

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.marketing.forms.configuration import Configuration


class LegalConsentCheckbox(object):
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
    openapi_types = {"required": "bool", "subscription_type_id": "int", "label": "str"}

    attribute_map = {"required": "required", "subscription_type_id": "subscriptionTypeId", "label": "label"}

    def __init__(self, required=None, subscription_type_id=None, label=None, local_vars_configuration=None):  # noqa: E501
        """LegalConsentCheckbox - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._required = None
        self._subscription_type_id = None
        self._label = None
        self.discriminator = None

        self.required = required
        self.subscription_type_id = subscription_type_id
        self.label = label

    @property
    def required(self):
        """Gets the required of this LegalConsentCheckbox.  # noqa: E501

        Whether this checkbox is required when submitting the form.  # noqa: E501

        :return: The required of this LegalConsentCheckbox.  # noqa: E501
        :rtype: bool
        """
        return self._required

    @required.setter
    def required(self, required):
        """Sets the required of this LegalConsentCheckbox.

        Whether this checkbox is required when submitting the form.  # noqa: E501

        :param required: The required of this LegalConsentCheckbox.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and required is None:  # noqa: E501
            raise ValueError("Invalid value for `required`, must not be `None`")  # noqa: E501

        self._required = required

    @property
    def subscription_type_id(self):
        """Gets the subscription_type_id of this LegalConsentCheckbox.  # noqa: E501


        :return: The subscription_type_id of this LegalConsentCheckbox.  # noqa: E501
        :rtype: int
        """
        return self._subscription_type_id

    @subscription_type_id.setter
    def subscription_type_id(self, subscription_type_id):
        """Sets the subscription_type_id of this LegalConsentCheckbox.


        :param subscription_type_id: The subscription_type_id of this LegalConsentCheckbox.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and subscription_type_id is None:  # noqa: E501
            raise ValueError("Invalid value for `subscription_type_id`, must not be `None`")  # noqa: E501

        self._subscription_type_id = subscription_type_id

    @property
    def label(self):
        """Gets the label of this LegalConsentCheckbox.  # noqa: E501

        The main label for the form field.  # noqa: E501

        :return: The label of this LegalConsentCheckbox.  # noqa: E501
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this LegalConsentCheckbox.

        The main label for the form field.  # noqa: E501

        :param label: The label of this LegalConsentCheckbox.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and label is None:  # noqa: E501
            raise ValueError("Invalid value for `label`, must not be `None`")  # noqa: E501

        self._label = label

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
        if not isinstance(other, LegalConsentCheckbox):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LegalConsentCheckbox):
            return True

        return self.to_dict() != other.to_dict()
