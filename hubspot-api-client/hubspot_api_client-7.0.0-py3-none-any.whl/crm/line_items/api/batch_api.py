# coding: utf-8

"""
    Line Items

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from hubspot.crm.line_items.api_client import ApiClient
from hubspot.crm.line_items.exceptions import ApiTypeError, ApiValueError


class BatchApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def archive(self, batch_input_simple_public_object_id, **kwargs):  # noqa: E501
        """Archive a batch of line items by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive(batch_input_simple_public_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectId batch_input_simple_public_object_id: (required)
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
        return self.archive_with_http_info(batch_input_simple_public_object_id, **kwargs)  # noqa: E501

    def archive_with_http_info(self, batch_input_simple_public_object_id, **kwargs):  # noqa: E501
        """Archive a batch of line items by ID  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive_with_http_info(batch_input_simple_public_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectId batch_input_simple_public_object_id: (required)
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

        all_params = ["batch_input_simple_public_object_id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method archive" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'batch_input_simple_public_object_id' is set
        if self.api_client.client_side_validation and (
            "batch_input_simple_public_object_id" not in local_var_params or local_var_params["batch_input_simple_public_object_id"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `batch_input_simple_public_object_id` when calling `archive`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "batch_input_simple_public_object_id" in local_var_params:
            body_params = local_var_params["batch_input_simple_public_object_id"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/objects/line_items/batch/archive",
            "POST",
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

    def create(self, batch_input_simple_public_object_input, **kwargs):  # noqa: E501
        """Create a batch of line items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(batch_input_simple_public_object_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectInput batch_input_simple_public_object_input: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: BatchResponseSimplePublicObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.create_with_http_info(batch_input_simple_public_object_input, **kwargs)  # noqa: E501

    def create_with_http_info(self, batch_input_simple_public_object_input, **kwargs):  # noqa: E501
        """Create a batch of line items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(batch_input_simple_public_object_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectInput batch_input_simple_public_object_input: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(BatchResponseSimplePublicObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["batch_input_simple_public_object_input"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method create" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'batch_input_simple_public_object_input' is set
        if self.api_client.client_side_validation and (
            "batch_input_simple_public_object_input" not in local_var_params or local_var_params["batch_input_simple_public_object_input"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `batch_input_simple_public_object_input` when calling `create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "batch_input_simple_public_object_input" in local_var_params:
            body_params = local_var_params["batch_input_simple_public_object_input"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/objects/line_items/batch/create",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="BatchResponseSimplePublicObject",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def read(self, batch_read_input_simple_public_object_id, **kwargs):  # noqa: E501
        """Read a batch of line items by internal ID, or unique property values  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read(batch_read_input_simple_public_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchReadInputSimplePublicObjectId batch_read_input_simple_public_object_id: (required)
        :param bool archived: Whether to return only results that have been archived.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: BatchResponseSimplePublicObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.read_with_http_info(batch_read_input_simple_public_object_id, **kwargs)  # noqa: E501

    def read_with_http_info(self, batch_read_input_simple_public_object_id, **kwargs):  # noqa: E501
        """Read a batch of line items by internal ID, or unique property values  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.read_with_http_info(batch_read_input_simple_public_object_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchReadInputSimplePublicObjectId batch_read_input_simple_public_object_id: (required)
        :param bool archived: Whether to return only results that have been archived.
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(BatchResponseSimplePublicObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["batch_read_input_simple_public_object_id", "archived"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method read" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'batch_read_input_simple_public_object_id' is set
        if self.api_client.client_side_validation and (
            "batch_read_input_simple_public_object_id" not in local_var_params or local_var_params["batch_read_input_simple_public_object_id"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `batch_read_input_simple_public_object_id` when calling `read`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if "archived" in local_var_params and local_var_params["archived"] is not None:  # noqa: E501
            query_params.append(("archived", local_var_params["archived"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "batch_read_input_simple_public_object_id" in local_var_params:
            body_params = local_var_params["batch_read_input_simple_public_object_id"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/objects/line_items/batch/read",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="BatchResponseSimplePublicObject",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def update(self, batch_input_simple_public_object_batch_input, **kwargs):  # noqa: E501
        """Update a batch of line items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update(batch_input_simple_public_object_batch_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectBatchInput batch_input_simple_public_object_batch_input: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: BatchResponseSimplePublicObject
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.update_with_http_info(batch_input_simple_public_object_batch_input, **kwargs)  # noqa: E501

    def update_with_http_info(self, batch_input_simple_public_object_batch_input, **kwargs):  # noqa: E501
        """Update a batch of line items  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_with_http_info(batch_input_simple_public_object_batch_input, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param BatchInputSimplePublicObjectBatchInput batch_input_simple_public_object_batch_input: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(BatchResponseSimplePublicObject, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["batch_input_simple_public_object_batch_input"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method update" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'batch_input_simple_public_object_batch_input' is set
        if self.api_client.client_side_validation and (
            "batch_input_simple_public_object_batch_input" not in local_var_params or local_var_params["batch_input_simple_public_object_batch_input"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `batch_input_simple_public_object_batch_input` when calling `update`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "batch_input_simple_public_object_batch_input" in local_var_params:
            body_params = local_var_params["batch_input_simple_public_object_batch_input"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/objects/line_items/batch/update",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="BatchResponseSimplePublicObject",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
