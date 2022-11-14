# coding: utf-8

"""
    UltraCart Rest API V2

    UltraCart REST API Version 2  # noqa: E501

    OpenAPI spec version: 2.0.0
    Contact: support@ultracart.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class CartSettingsPaymentAmazon(object):
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
        'amazon_button_url': 'str',
        'amazon_merchant_id': 'str',
        'amazon_widget_url': 'str'
    }

    attribute_map = {
        'amazon_button_url': 'amazon_button_url',
        'amazon_merchant_id': 'amazon_merchant_id',
        'amazon_widget_url': 'amazon_widget_url'
    }

    def __init__(self, amazon_button_url=None, amazon_merchant_id=None, amazon_widget_url=None):  # noqa: E501
        """CartSettingsPaymentAmazon - a model defined in Swagger"""  # noqa: E501

        self._amazon_button_url = None
        self._amazon_merchant_id = None
        self._amazon_widget_url = None
        self.discriminator = None

        if amazon_button_url is not None:
            self.amazon_button_url = amazon_button_url
        if amazon_merchant_id is not None:
            self.amazon_merchant_id = amazon_merchant_id
        if amazon_widget_url is not None:
            self.amazon_widget_url = amazon_widget_url

    @property
    def amazon_button_url(self):
        """Gets the amazon_button_url of this CartSettingsPaymentAmazon.  # noqa: E501

        Amazon button URL  # noqa: E501

        :return: The amazon_button_url of this CartSettingsPaymentAmazon.  # noqa: E501
        :rtype: str
        """
        return self._amazon_button_url

    @amazon_button_url.setter
    def amazon_button_url(self, amazon_button_url):
        """Sets the amazon_button_url of this CartSettingsPaymentAmazon.

        Amazon button URL  # noqa: E501

        :param amazon_button_url: The amazon_button_url of this CartSettingsPaymentAmazon.  # noqa: E501
        :type: str
        """

        self._amazon_button_url = amazon_button_url

    @property
    def amazon_merchant_id(self):
        """Gets the amazon_merchant_id of this CartSettingsPaymentAmazon.  # noqa: E501

        Amazon merchant ID  # noqa: E501

        :return: The amazon_merchant_id of this CartSettingsPaymentAmazon.  # noqa: E501
        :rtype: str
        """
        return self._amazon_merchant_id

    @amazon_merchant_id.setter
    def amazon_merchant_id(self, amazon_merchant_id):
        """Sets the amazon_merchant_id of this CartSettingsPaymentAmazon.

        Amazon merchant ID  # noqa: E501

        :param amazon_merchant_id: The amazon_merchant_id of this CartSettingsPaymentAmazon.  # noqa: E501
        :type: str
        """

        self._amazon_merchant_id = amazon_merchant_id

    @property
    def amazon_widget_url(self):
        """Gets the amazon_widget_url of this CartSettingsPaymentAmazon.  # noqa: E501

        Amazon widget URL  # noqa: E501

        :return: The amazon_widget_url of this CartSettingsPaymentAmazon.  # noqa: E501
        :rtype: str
        """
        return self._amazon_widget_url

    @amazon_widget_url.setter
    def amazon_widget_url(self, amazon_widget_url):
        """Sets the amazon_widget_url of this CartSettingsPaymentAmazon.

        Amazon widget URL  # noqa: E501

        :param amazon_widget_url: The amazon_widget_url of this CartSettingsPaymentAmazon.  # noqa: E501
        :type: str
        """

        self._amazon_widget_url = amazon_widget_url

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
        if issubclass(CartSettingsPaymentAmazon, dict):
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
        if not isinstance(other, CartSettingsPaymentAmazon):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
