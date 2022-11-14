# coding: utf-8

"""
    CRM Objects

    CRM objects such as companies, contacts, deals, line items, products, tickets, and quotes are standard objects in HubSpot’s CRM. These core building blocks support custom properties, store critical information, and play a central role in the HubSpot application.  ## Supported Object Types  This API provides access to collections of CRM objects, which return a map of property names to values. Each object type has its own set of default properties, which can be found by exploring the [CRM Object Properties API](https://developers.hubspot.com/docs/methods/crm-properties/crm-properties-overview).  |Object Type |Properties returned by default | |--|--| | `companies` | `name`, `domain` | | `contacts` | `firstname`, `lastname`, `email` | | `deals` | `dealname`, `amount`, `closedate`, `pipeline`, `dealstage` | | `products` | `name`, `description`, `price` | | `tickets` | `content`, `hs_pipeline`, `hs_pipeline_stage`, `hs_ticket_category`, `hs_ticket_priority`, `subject` |  Find a list of all properties for an object type using the [CRM Object Properties](https://developers.hubspot.com/docs/methods/crm-properties/get-properties) API. e.g. `GET https://api.hubapi.com/properties/v2/companies/properties`. Change the properties returned in the response using the `properties` array in the request body.  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.crm.objects.configuration import Configuration


class BatchReadInputSimplePublicObjectId(object):
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
    openapi_types = {"properties": "list[str]", "properties_with_history": "list[str]", "id_property": "str", "inputs": "list[SimplePublicObjectId]"}

    attribute_map = {"properties": "properties", "properties_with_history": "propertiesWithHistory", "id_property": "idProperty", "inputs": "inputs"}

    def __init__(self, properties=None, properties_with_history=None, id_property=None, inputs=None, local_vars_configuration=None):  # noqa: E501
        """BatchReadInputSimplePublicObjectId - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._properties = None
        self._properties_with_history = None
        self._id_property = None
        self._inputs = None
        self.discriminator = None

        self.properties = properties
        self.properties_with_history = properties_with_history
        if id_property is not None:
            self.id_property = id_property
        self.inputs = inputs

    @property
    def properties(self):
        """Gets the properties of this BatchReadInputSimplePublicObjectId.  # noqa: E501


        :return: The properties of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :rtype: list[str]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this BatchReadInputSimplePublicObjectId.


        :param properties: The properties of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and properties is None:  # noqa: E501
            raise ValueError("Invalid value for `properties`, must not be `None`")  # noqa: E501

        self._properties = properties

    @property
    def properties_with_history(self):
        """Gets the properties_with_history of this BatchReadInputSimplePublicObjectId.  # noqa: E501


        :return: The properties_with_history of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :rtype: list[str]
        """
        return self._properties_with_history

    @properties_with_history.setter
    def properties_with_history(self, properties_with_history):
        """Sets the properties_with_history of this BatchReadInputSimplePublicObjectId.


        :param properties_with_history: The properties_with_history of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and properties_with_history is None:  # noqa: E501
            raise ValueError("Invalid value for `properties_with_history`, must not be `None`")  # noqa: E501

        self._properties_with_history = properties_with_history

    @property
    def id_property(self):
        """Gets the id_property of this BatchReadInputSimplePublicObjectId.  # noqa: E501


        :return: The id_property of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :rtype: str
        """
        return self._id_property

    @id_property.setter
    def id_property(self, id_property):
        """Sets the id_property of this BatchReadInputSimplePublicObjectId.


        :param id_property: The id_property of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :type: str
        """

        self._id_property = id_property

    @property
    def inputs(self):
        """Gets the inputs of this BatchReadInputSimplePublicObjectId.  # noqa: E501


        :return: The inputs of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :rtype: list[SimplePublicObjectId]
        """
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        """Sets the inputs of this BatchReadInputSimplePublicObjectId.


        :param inputs: The inputs of this BatchReadInputSimplePublicObjectId.  # noqa: E501
        :type: list[SimplePublicObjectId]
        """
        if self.local_vars_configuration.client_side_validation and inputs is None:  # noqa: E501
            raise ValueError("Invalid value for `inputs`, must not be `None`")  # noqa: E501

        self._inputs = inputs

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
        if not isinstance(other, BatchReadInputSimplePublicObjectId):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BatchReadInputSimplePublicObjectId):
            return True

        return self.to_dict() != other.to_dict()
