# coding: utf-8

"""
    Schemas

    The CRM uses schemas to define how custom objects should store and represent information in the HubSpot CRM. Schemas define details about an object's type, properties, and associations. The schema can be uniquely identified by its **object type ID**.  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from hubspot.crm.schemas.api_client import ApiClient
from hubspot.crm.schemas.exceptions import ApiTypeError, ApiValueError


class PublicObjectSchemasApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def purge(self, object_type, **kwargs):  # noqa: E501
        """purge  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.purge(object_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str object_type: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.purge_with_http_info(object_type, **kwargs)  # noqa: E501

    def purge_with_http_info(self, object_type, **kwargs):  # noqa: E501
        """purge  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.purge_with_http_info(object_type, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str object_type: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["object_type"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method purge" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'object_type' is set
        if self.api_client.client_side_validation and ("object_type" not in local_var_params or local_var_params["object_type"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `object_type` when calling `purge`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "object_type" in local_var_params:
            path_params["objectType"] = local_var_params["object_type"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/schemas/{objectType}/purge",
            "DELETE",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
