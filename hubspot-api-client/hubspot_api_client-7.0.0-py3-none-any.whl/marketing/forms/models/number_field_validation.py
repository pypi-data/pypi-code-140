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


class NumberFieldValidation(object):
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
    openapi_types = {"min_allowed_digits": "int", "max_allowed_digits": "int"}

    attribute_map = {"min_allowed_digits": "minAllowedDigits", "max_allowed_digits": "maxAllowedDigits"}

    def __init__(self, min_allowed_digits=None, max_allowed_digits=None, local_vars_configuration=None):  # noqa: E501
        """NumberFieldValidation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._min_allowed_digits = None
        self._max_allowed_digits = None
        self.discriminator = None

        self.min_allowed_digits = min_allowed_digits
        self.max_allowed_digits = max_allowed_digits

    @property
    def min_allowed_digits(self):
        """Gets the min_allowed_digits of this NumberFieldValidation.  # noqa: E501


        :return: The min_allowed_digits of this NumberFieldValidation.  # noqa: E501
        :rtype: int
        """
        return self._min_allowed_digits

    @min_allowed_digits.setter
    def min_allowed_digits(self, min_allowed_digits):
        """Sets the min_allowed_digits of this NumberFieldValidation.


        :param min_allowed_digits: The min_allowed_digits of this NumberFieldValidation.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and min_allowed_digits is None:  # noqa: E501
            raise ValueError("Invalid value for `min_allowed_digits`, must not be `None`")  # noqa: E501

        self._min_allowed_digits = min_allowed_digits

    @property
    def max_allowed_digits(self):
        """Gets the max_allowed_digits of this NumberFieldValidation.  # noqa: E501


        :return: The max_allowed_digits of this NumberFieldValidation.  # noqa: E501
        :rtype: int
        """
        return self._max_allowed_digits

    @max_allowed_digits.setter
    def max_allowed_digits(self, max_allowed_digits):
        """Sets the max_allowed_digits of this NumberFieldValidation.


        :param max_allowed_digits: The max_allowed_digits of this NumberFieldValidation.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and max_allowed_digits is None:  # noqa: E501
            raise ValueError("Invalid value for `max_allowed_digits`, must not be `None`")  # noqa: E501

        self._max_allowed_digits = max_allowed_digits

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
        if not isinstance(other, NumberFieldValidation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, NumberFieldValidation):
            return True

        return self.to_dict() != other.to_dict()
