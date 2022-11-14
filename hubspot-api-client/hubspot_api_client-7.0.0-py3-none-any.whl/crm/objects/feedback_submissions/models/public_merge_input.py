# coding: utf-8

"""
    Feedback Submissions

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.crm.objects.feedback_submissions.configuration import Configuration


class PublicMergeInput(object):
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
    openapi_types = {"primary_object_id": "str", "object_id_to_merge": "str"}

    attribute_map = {"primary_object_id": "primaryObjectId", "object_id_to_merge": "objectIdToMerge"}

    def __init__(self, primary_object_id=None, object_id_to_merge=None, local_vars_configuration=None):  # noqa: E501
        """PublicMergeInput - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._primary_object_id = None
        self._object_id_to_merge = None
        self.discriminator = None

        self.primary_object_id = primary_object_id
        self.object_id_to_merge = object_id_to_merge

    @property
    def primary_object_id(self):
        """Gets the primary_object_id of this PublicMergeInput.  # noqa: E501


        :return: The primary_object_id of this PublicMergeInput.  # noqa: E501
        :rtype: str
        """
        return self._primary_object_id

    @primary_object_id.setter
    def primary_object_id(self, primary_object_id):
        """Sets the primary_object_id of this PublicMergeInput.


        :param primary_object_id: The primary_object_id of this PublicMergeInput.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and primary_object_id is None:  # noqa: E501
            raise ValueError("Invalid value for `primary_object_id`, must not be `None`")  # noqa: E501

        self._primary_object_id = primary_object_id

    @property
    def object_id_to_merge(self):
        """Gets the object_id_to_merge of this PublicMergeInput.  # noqa: E501


        :return: The object_id_to_merge of this PublicMergeInput.  # noqa: E501
        :rtype: str
        """
        return self._object_id_to_merge

    @object_id_to_merge.setter
    def object_id_to_merge(self, object_id_to_merge):
        """Sets the object_id_to_merge of this PublicMergeInput.


        :param object_id_to_merge: The object_id_to_merge of this PublicMergeInput.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and object_id_to_merge is None:  # noqa: E501
            raise ValueError("Invalid value for `object_id_to_merge`, must not be `None`")  # noqa: E501

        self._object_id_to_merge = object_id_to_merge

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
        if not isinstance(other, PublicMergeInput):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PublicMergeInput):
            return True

        return self.to_dict() != other.to_dict()
