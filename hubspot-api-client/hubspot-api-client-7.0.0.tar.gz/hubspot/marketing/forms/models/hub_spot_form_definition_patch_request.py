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


class HubSpotFormDefinitionPatchRequest(object):
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
        "name": "str",
        "field_groups": "list[FieldGroup]",
        "configuration": "HubSpotFormConfiguration",
        "display_options": "FormDisplayOptions",
        "legal_consent_options": "OneOfLegalConsentOptionsNoneLegalConsentOptionsLegitimateInterestLegalConsentOptionsExplicitConsentToProcessLegalConsentOptionsImplicitConsentToProcess",
        "archived": "bool",
    }

    attribute_map = {
        "name": "name",
        "field_groups": "fieldGroups",
        "configuration": "configuration",
        "display_options": "displayOptions",
        "legal_consent_options": "legalConsentOptions",
        "archived": "archived",
    }

    def __init__(self, name=None, field_groups=None, configuration=None, display_options=None, legal_consent_options=None, archived=None, local_vars_configuration=None):  # noqa: E501
        """HubSpotFormDefinitionPatchRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._field_groups = None
        self._configuration = None
        self._display_options = None
        self._legal_consent_options = None
        self._archived = None
        self.discriminator = None

        if name is not None:
            self.name = name
        if field_groups is not None:
            self.field_groups = field_groups
        if configuration is not None:
            self.configuration = configuration
        if display_options is not None:
            self.display_options = display_options
        if legal_consent_options is not None:
            self.legal_consent_options = legal_consent_options
        if archived is not None:
            self.archived = archived

    @property
    def name(self):
        """Gets the name of this HubSpotFormDefinitionPatchRequest.  # noqa: E501

        The name of the form. Expected to be unique for a hub.  # noqa: E501

        :return: The name of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this HubSpotFormDefinitionPatchRequest.

        The name of the form. Expected to be unique for a hub.  # noqa: E501

        :param name: The name of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def field_groups(self):
        """Gets the field_groups of this HubSpotFormDefinitionPatchRequest.  # noqa: E501

        The fields in the form, grouped in rows.  # noqa: E501

        :return: The field_groups of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: list[FieldGroup]
        """
        return self._field_groups

    @field_groups.setter
    def field_groups(self, field_groups):
        """Sets the field_groups of this HubSpotFormDefinitionPatchRequest.

        The fields in the form, grouped in rows.  # noqa: E501

        :param field_groups: The field_groups of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: list[FieldGroup]
        """

        self._field_groups = field_groups

    @property
    def configuration(self):
        """Gets the configuration of this HubSpotFormDefinitionPatchRequest.  # noqa: E501


        :return: The configuration of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: HubSpotFormConfiguration
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """Sets the configuration of this HubSpotFormDefinitionPatchRequest.


        :param configuration: The configuration of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: HubSpotFormConfiguration
        """

        self._configuration = configuration

    @property
    def display_options(self):
        """Gets the display_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501


        :return: The display_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: FormDisplayOptions
        """
        return self._display_options

    @display_options.setter
    def display_options(self, display_options):
        """Sets the display_options of this HubSpotFormDefinitionPatchRequest.


        :param display_options: The display_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: FormDisplayOptions
        """

        self._display_options = display_options

    @property
    def legal_consent_options(self):
        """Gets the legal_consent_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501


        :return: The legal_consent_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: OneOfLegalConsentOptionsNoneLegalConsentOptionsLegitimateInterestLegalConsentOptionsExplicitConsentToProcessLegalConsentOptionsImplicitConsentToProcess
        """
        return self._legal_consent_options

    @legal_consent_options.setter
    def legal_consent_options(self, legal_consent_options):
        """Sets the legal_consent_options of this HubSpotFormDefinitionPatchRequest.


        :param legal_consent_options: The legal_consent_options of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: OneOfLegalConsentOptionsNoneLegalConsentOptionsLegitimateInterestLegalConsentOptionsExplicitConsentToProcessLegalConsentOptionsImplicitConsentToProcess
        """

        self._legal_consent_options = legal_consent_options

    @property
    def archived(self):
        """Gets the archived of this HubSpotFormDefinitionPatchRequest.  # noqa: E501

        Whether this form is archived.  # noqa: E501

        :return: The archived of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :rtype: bool
        """
        return self._archived

    @archived.setter
    def archived(self, archived):
        """Sets the archived of this HubSpotFormDefinitionPatchRequest.

        Whether this form is archived.  # noqa: E501

        :param archived: The archived of this HubSpotFormDefinitionPatchRequest.  # noqa: E501
        :type: bool
        """

        self._archived = archived

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
        if not isinstance(other, HubSpotFormDefinitionPatchRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HubSpotFormDefinitionPatchRequest):
            return True

        return self.to_dict() != other.to_dict()
