# coding: utf-8

"""
    Blog Post endpoints

    Use these endpoints for interacting with Blog Posts, Blog Authors, and Blog Tags  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.cms.blogs.blog_posts.configuration import Configuration


class BackgroundImage(object):
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
    openapi_types = {"image_url": "str", "background_size": "str", "background_position": "str"}

    attribute_map = {"image_url": "imageUrl", "background_size": "backgroundSize", "background_position": "backgroundPosition"}

    def __init__(self, image_url=None, background_size=None, background_position=None, local_vars_configuration=None):  # noqa: E501
        """BackgroundImage - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._image_url = None
        self._background_size = None
        self._background_position = None
        self.discriminator = None

        self.image_url = image_url
        self.background_size = background_size
        self.background_position = background_position

    @property
    def image_url(self):
        """Gets the image_url of this BackgroundImage.  # noqa: E501


        :return: The image_url of this BackgroundImage.  # noqa: E501
        :rtype: str
        """
        return self._image_url

    @image_url.setter
    def image_url(self, image_url):
        """Sets the image_url of this BackgroundImage.


        :param image_url: The image_url of this BackgroundImage.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and image_url is None:  # noqa: E501
            raise ValueError("Invalid value for `image_url`, must not be `None`")  # noqa: E501

        self._image_url = image_url

    @property
    def background_size(self):
        """Gets the background_size of this BackgroundImage.  # noqa: E501


        :return: The background_size of this BackgroundImage.  # noqa: E501
        :rtype: str
        """
        return self._background_size

    @background_size.setter
    def background_size(self, background_size):
        """Sets the background_size of this BackgroundImage.


        :param background_size: The background_size of this BackgroundImage.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and background_size is None:  # noqa: E501
            raise ValueError("Invalid value for `background_size`, must not be `None`")  # noqa: E501

        self._background_size = background_size

    @property
    def background_position(self):
        """Gets the background_position of this BackgroundImage.  # noqa: E501


        :return: The background_position of this BackgroundImage.  # noqa: E501
        :rtype: str
        """
        return self._background_position

    @background_position.setter
    def background_position(self, background_position):
        """Sets the background_position of this BackgroundImage.


        :param background_position: The background_position of this BackgroundImage.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and background_position is None:  # noqa: E501
            raise ValueError("Invalid value for `background_position`, must not be `None`")  # noqa: E501
        allowed_values = ["TOP_LEFT", "TOP_CENTER", "TOP_RIGHT", "MIDDLE_LEFT", "MIDDLE_CENTER", "MIDDLE_RIGHT", "BOTTOM_LEFT", "BOTTOM_CENTER", "BOTTOM_RIGHT"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and background_position not in allowed_values:  # noqa: E501
            raise ValueError("Invalid value for `background_position` ({0}), must be one of {1}".format(background_position, allowed_values))  # noqa: E501

        self._background_position = background_position

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
        if not isinstance(other, BackgroundImage):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BackgroundImage):
            return True

        return self.to_dict() != other.to_dict()
