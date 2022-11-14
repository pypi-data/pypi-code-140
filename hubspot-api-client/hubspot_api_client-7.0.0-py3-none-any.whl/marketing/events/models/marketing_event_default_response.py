# coding: utf-8

"""
    Marketing Events Extension

    These APIs allow you to interact with HubSpot's Marketing Events Extension. It allows you to: * Create, Read or update Marketing Event information in HubSpot * Specify whether a HubSpot contact has registered, attended or cancelled a registration to a Marketing Event. * Specify a URL that can be called to get the details of a Marketing Event.   # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from hubspot.marketing.events.configuration import Configuration


class MarketingEventDefaultResponse(object):
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
    openapi_types = {
        "event_name": "str",
        "event_type": "str",
        "start_date_time": "datetime",
        "end_date_time": "datetime",
        "event_organizer": "str",
        "event_description": "str",
        "event_url": "str",
        "event_cancelled": "bool",
        "custom_properties": "list[PropertyValue]",
    }

    attribute_map = {
        "event_name": "eventName",
        "event_type": "eventType",
        "start_date_time": "startDateTime",
        "end_date_time": "endDateTime",
        "event_organizer": "eventOrganizer",
        "event_description": "eventDescription",
        "event_url": "eventUrl",
        "event_cancelled": "eventCancelled",
        "custom_properties": "customProperties",
    }

    def __init__(
        self,
        event_name=None,
        event_type=None,
        start_date_time=None,
        end_date_time=None,
        event_organizer=None,
        event_description=None,
        event_url=None,
        event_cancelled=None,
        custom_properties=None,
        local_vars_configuration=None,
    ):  # noqa: E501
        """MarketingEventDefaultResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._event_name = None
        self._event_type = None
        self._start_date_time = None
        self._end_date_time = None
        self._event_organizer = None
        self._event_description = None
        self._event_url = None
        self._event_cancelled = None
        self._custom_properties = None
        self.discriminator = None

        self.event_name = event_name
        if event_type is not None:
            self.event_type = event_type
        if start_date_time is not None:
            self.start_date_time = start_date_time
        if end_date_time is not None:
            self.end_date_time = end_date_time
        self.event_organizer = event_organizer
        if event_description is not None:
            self.event_description = event_description
        if event_url is not None:
            self.event_url = event_url
        if event_cancelled is not None:
            self.event_cancelled = event_cancelled
        if custom_properties is not None:
            self.custom_properties = custom_properties

    @property
    def event_name(self):
        """Gets the event_name of this MarketingEventDefaultResponse.  # noqa: E501

        The name of the marketing event.  # noqa: E501

        :return: The event_name of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: str
        """
        return self._event_name

    @event_name.setter
    def event_name(self, event_name):
        """Sets the event_name of this MarketingEventDefaultResponse.

        The name of the marketing event.  # noqa: E501

        :param event_name: The event_name of this MarketingEventDefaultResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and event_name is None:  # noqa: E501
            raise ValueError("Invalid value for `event_name`, must not be `None`")  # noqa: E501

        self._event_name = event_name

    @property
    def event_type(self):
        """Gets the event_type of this MarketingEventDefaultResponse.  # noqa: E501

        The type of the marketing event.  # noqa: E501

        :return: The event_type of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: str
        """
        return self._event_type

    @event_type.setter
    def event_type(self, event_type):
        """Sets the event_type of this MarketingEventDefaultResponse.

        The type of the marketing event.  # noqa: E501

        :param event_type: The event_type of this MarketingEventDefaultResponse.  # noqa: E501
        :type: str
        """

        self._event_type = event_type

    @property
    def start_date_time(self):
        """Gets the start_date_time of this MarketingEventDefaultResponse.  # noqa: E501

        The start date and time of the marketing event.  # noqa: E501

        :return: The start_date_time of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date_time

    @start_date_time.setter
    def start_date_time(self, start_date_time):
        """Sets the start_date_time of this MarketingEventDefaultResponse.

        The start date and time of the marketing event.  # noqa: E501

        :param start_date_time: The start_date_time of this MarketingEventDefaultResponse.  # noqa: E501
        :type: datetime
        """

        self._start_date_time = start_date_time

    @property
    def end_date_time(self):
        """Gets the end_date_time of this MarketingEventDefaultResponse.  # noqa: E501

        The end date and time of the marketing event.  # noqa: E501

        :return: The end_date_time of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._end_date_time

    @end_date_time.setter
    def end_date_time(self, end_date_time):
        """Sets the end_date_time of this MarketingEventDefaultResponse.

        The end date and time of the marketing event.  # noqa: E501

        :param end_date_time: The end_date_time of this MarketingEventDefaultResponse.  # noqa: E501
        :type: datetime
        """

        self._end_date_time = end_date_time

    @property
    def event_organizer(self):
        """Gets the event_organizer of this MarketingEventDefaultResponse.  # noqa: E501

        The name of the organizer of the marketing event.  # noqa: E501

        :return: The event_organizer of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: str
        """
        return self._event_organizer

    @event_organizer.setter
    def event_organizer(self, event_organizer):
        """Sets the event_organizer of this MarketingEventDefaultResponse.

        The name of the organizer of the marketing event.  # noqa: E501

        :param event_organizer: The event_organizer of this MarketingEventDefaultResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and event_organizer is None:  # noqa: E501
            raise ValueError("Invalid value for `event_organizer`, must not be `None`")  # noqa: E501

        self._event_organizer = event_organizer

    @property
    def event_description(self):
        """Gets the event_description of this MarketingEventDefaultResponse.  # noqa: E501

        The description of the marketing event.  # noqa: E501

        :return: The event_description of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: str
        """
        return self._event_description

    @event_description.setter
    def event_description(self, event_description):
        """Sets the event_description of this MarketingEventDefaultResponse.

        The description of the marketing event.  # noqa: E501

        :param event_description: The event_description of this MarketingEventDefaultResponse.  # noqa: E501
        :type: str
        """

        self._event_description = event_description

    @property
    def event_url(self):
        """Gets the event_url of this MarketingEventDefaultResponse.  # noqa: E501

        The URL in the external event application where the marketing event can be managed.  # noqa: E501

        :return: The event_url of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: str
        """
        return self._event_url

    @event_url.setter
    def event_url(self, event_url):
        """Sets the event_url of this MarketingEventDefaultResponse.

        The URL in the external event application where the marketing event can be managed.  # noqa: E501

        :param event_url: The event_url of this MarketingEventDefaultResponse.  # noqa: E501
        :type: str
        """

        self._event_url = event_url

    @property
    def event_cancelled(self):
        """Gets the event_cancelled of this MarketingEventDefaultResponse.  # noqa: E501

        Indicates if the marketing event has been cancelled.  # noqa: E501

        :return: The event_cancelled of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: bool
        """
        return self._event_cancelled

    @event_cancelled.setter
    def event_cancelled(self, event_cancelled):
        """Sets the event_cancelled of this MarketingEventDefaultResponse.

        Indicates if the marketing event has been cancelled.  # noqa: E501

        :param event_cancelled: The event_cancelled of this MarketingEventDefaultResponse.  # noqa: E501
        :type: bool
        """

        self._event_cancelled = event_cancelled

    @property
    def custom_properties(self):
        """Gets the custom_properties of this MarketingEventDefaultResponse.  # noqa: E501

        A list of PropertyValues. These can be whatever kind of property names and values you want. However, they must already exist on the HubSpot account's definition of the MarketingEvent Object. If they don't they will be filtered out and not set. In order to do this you'll need to create a new PropertyGroup on the HubSpot account's MarketingEvent object for your specific app and create the Custom Property you want to track on that HubSpot account. Do not create any new default properties on the MarketingEvent object as that will apply to all HubSpot accounts.   # noqa: E501

        :return: The custom_properties of this MarketingEventDefaultResponse.  # noqa: E501
        :rtype: list[PropertyValue]
        """
        return self._custom_properties

    @custom_properties.setter
    def custom_properties(self, custom_properties):
        """Sets the custom_properties of this MarketingEventDefaultResponse.

        A list of PropertyValues. These can be whatever kind of property names and values you want. However, they must already exist on the HubSpot account's definition of the MarketingEvent Object. If they don't they will be filtered out and not set. In order to do this you'll need to create a new PropertyGroup on the HubSpot account's MarketingEvent object for your specific app and create the Custom Property you want to track on that HubSpot account. Do not create any new default properties on the MarketingEvent object as that will apply to all HubSpot accounts.   # noqa: E501

        :param custom_properties: The custom_properties of this MarketingEventDefaultResponse.  # noqa: E501
        :type: list[PropertyValue]
        """

        self._custom_properties = custom_properties

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
        if not isinstance(other, MarketingEventDefaultResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarketingEventDefaultResponse):
            return True

        return self.to_dict() != other.to_dict()
