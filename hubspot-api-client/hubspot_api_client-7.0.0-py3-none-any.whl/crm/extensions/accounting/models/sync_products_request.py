# coding: utf-8

"""
    Accounting Extension

    These APIs allow you to interact with HubSpot's Accounting Extension. It allows you to: * Specify the URLs that HubSpot will use when making webhook requests to your external accounting system. * Respond to webhook calls made to your external accounting system by HubSpot   # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.crm.extensions.accounting.configuration import Configuration


class SyncProductsRequest(object):
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
    openapi_types = {"account_id": "str", "products": "list[UpdatedProduct]"}

    attribute_map = {"account_id": "accountId", "products": "products"}

    def __init__(self, account_id=None, products=None, local_vars_configuration=None):  # noqa: E501
        """SyncProductsRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._account_id = None
        self._products = None
        self.discriminator = None

        self.account_id = account_id
        self.products = products

    @property
    def account_id(self):
        """Gets the account_id of this SyncProductsRequest.  # noqa: E501

        The ID of the account in the external accounting system. This is the value that will be passed as `accountId` for all outbound calls for the user from HubSpot to the external accounting system.  # noqa: E501

        :return: The account_id of this SyncProductsRequest.  # noqa: E501
        :rtype: str
        """
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        """Sets the account_id of this SyncProductsRequest.

        The ID of the account in the external accounting system. This is the value that will be passed as `accountId` for all outbound calls for the user from HubSpot to the external accounting system.  # noqa: E501

        :param account_id: The account_id of this SyncProductsRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and account_id is None:  # noqa: E501
            raise ValueError("Invalid value for `account_id`, must not be `None`")  # noqa: E501

        self._account_id = account_id

    @property
    def products(self):
        """Gets the products of this SyncProductsRequest.  # noqa: E501

        A list of products to be imported.  # noqa: E501

        :return: The products of this SyncProductsRequest.  # noqa: E501
        :rtype: list[UpdatedProduct]
        """
        return self._products

    @products.setter
    def products(self, products):
        """Sets the products of this SyncProductsRequest.

        A list of products to be imported.  # noqa: E501

        :param products: The products of this SyncProductsRequest.  # noqa: E501
        :type: list[UpdatedProduct]
        """
        if self.local_vars_configuration.client_side_validation and products is None:  # noqa: E501
            raise ValueError("Invalid value for `products`, must not be `None`")  # noqa: E501

        self._products = products

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
        if not isinstance(other, SyncProductsRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SyncProductsRequest):
            return True

        return self.to_dict() != other.to_dict()
