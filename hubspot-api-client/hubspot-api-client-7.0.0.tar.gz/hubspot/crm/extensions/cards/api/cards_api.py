# coding: utf-8

"""
    CRM cards

    Allows an app to extend the CRM UI by surfacing custom cards in the sidebar of record pages. These cards are defined up-front as part of app configuration, then populated by external data fetch requests when the record page is accessed by a user.  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from hubspot.crm.extensions.cards.api_client import ApiClient
from hubspot.crm.extensions.cards.exceptions import ApiTypeError, ApiValueError


class CardsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def archive(self, app_id, card_id, **kwargs):  # noqa: E501
        """Delete a card  # noqa: E501

        Permanently deletes a card definition with the given ID. Once deleted, data fetch requests for this card will no longer be sent to your service. This can't be undone.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive(app_id, card_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the card to delete. (required)
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
        return self.archive_with_http_info(app_id, card_id, **kwargs)  # noqa: E501

    def archive_with_http_info(self, app_id, card_id, **kwargs):  # noqa: E501
        """Delete a card  # noqa: E501

        Permanently deletes a card definition with the given ID. Once deleted, data fetch requests for this card will no longer be sent to your service. This can't be undone.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.archive_with_http_info(app_id, card_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the card to delete. (required)
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

        all_params = ["app_id", "card_id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method archive" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ("app_id" not in local_var_params or local_var_params["app_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `archive`")  # noqa: E501
        # verify the required parameter 'card_id' is set
        if self.api_client.client_side_validation and ("card_id" not in local_var_params or local_var_params["card_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `card_id` when calling `archive`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "app_id" in local_var_params:
            path_params["appId"] = local_var_params["app_id"]  # noqa: E501
        if "card_id" in local_var_params:
            path_params["cardId"] = local_var_params["card_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["developer_hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/extensions/cards/{appId}/{cardId}",
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

    def create(self, app_id, card_create_request, **kwargs):  # noqa: E501
        """Create a new card  # noqa: E501

        Defines a new card that will become active on an account when this app is installed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create(app_id, card_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param CardCreateRequest card_create_request: The new card definition. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.create_with_http_info(app_id, card_create_request, **kwargs)  # noqa: E501

    def create_with_http_info(self, app_id, card_create_request, **kwargs):  # noqa: E501
        """Create a new card  # noqa: E501

        Defines a new card that will become active on an account when this app is installed.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.create_with_http_info(app_id, card_create_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param CardCreateRequest card_create_request: The new card definition. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CardResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["app_id", "card_create_request"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method create" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ("app_id" not in local_var_params or local_var_params["app_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `create`")  # noqa: E501
        # verify the required parameter 'card_create_request' is set
        if self.api_client.client_side_validation and ("card_create_request" not in local_var_params or local_var_params["card_create_request"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `card_create_request` when calling `create`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "app_id" in local_var_params:
            path_params["appId"] = local_var_params["app_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "card_create_request" in local_var_params:
            body_params = local_var_params["card_create_request"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["developer_hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/extensions/cards/{appId}",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CardResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_all(self, app_id, **kwargs):  # noqa: E501
        """Get all cards  # noqa: E501

        Returns a list of cards for a given app.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all(app_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CardListResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_all_with_http_info(app_id, **kwargs)  # noqa: E501

    def get_all_with_http_info(self, app_id, **kwargs):  # noqa: E501
        """Get all cards  # noqa: E501

        Returns a list of cards for a given app.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_all_with_http_info(app_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CardListResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["app_id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method get_all" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ("app_id" not in local_var_params or local_var_params["app_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `get_all`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "app_id" in local_var_params:
            path_params["appId"] = local_var_params["app_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["developer_hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/extensions/cards/{appId}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CardListResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_by_id(self, app_id, card_id, **kwargs):  # noqa: E501
        """Get a card.  # noqa: E501

        Returns the definition for a card with the given ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_by_id(app_id, card_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the target card. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_by_id_with_http_info(app_id, card_id, **kwargs)  # noqa: E501

    def get_by_id_with_http_info(self, app_id, card_id, **kwargs):  # noqa: E501
        """Get a card.  # noqa: E501

        Returns the definition for a card with the given ID.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_by_id_with_http_info(app_id, card_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the target card. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CardResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["app_id", "card_id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method get_by_id" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ("app_id" not in local_var_params or local_var_params["app_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `get_by_id`")  # noqa: E501
        # verify the required parameter 'card_id' is set
        if self.api_client.client_side_validation and ("card_id" not in local_var_params or local_var_params["card_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `card_id` when calling `get_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "app_id" in local_var_params:
            path_params["appId"] = local_var_params["app_id"]  # noqa: E501
        if "card_id" in local_var_params:
            path_params["cardId"] = local_var_params["card_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["developer_hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/extensions/cards/{appId}/{cardId}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CardResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def update(self, app_id, card_id, card_patch_request, **kwargs):  # noqa: E501
        """Update a card  # noqa: E501

        Update a card definition with new details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update(app_id, card_id, card_patch_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the card to update. (required)
        :param CardPatchRequest card_patch_request: Card definition fields to be updated. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CardResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.update_with_http_info(app_id, card_id, card_patch_request, **kwargs)  # noqa: E501

    def update_with_http_info(self, app_id, card_id, card_patch_request, **kwargs):  # noqa: E501
        """Update a card  # noqa: E501

        Update a card definition with new details.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.update_with_http_info(app_id, card_id, card_patch_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param int app_id: The ID of the target app. (required)
        :param str card_id: The ID of the card to update. (required)
        :param CardPatchRequest card_patch_request: Card definition fields to be updated. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(CardResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["app_id", "card_id", "card_patch_request"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method update" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'app_id' is set
        if self.api_client.client_side_validation and ("app_id" not in local_var_params or local_var_params["app_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `app_id` when calling `update`")  # noqa: E501
        # verify the required parameter 'card_id' is set
        if self.api_client.client_side_validation and ("card_id" not in local_var_params or local_var_params["card_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `card_id` when calling `update`")  # noqa: E501
        # verify the required parameter 'card_patch_request' is set
        if self.api_client.client_side_validation and ("card_patch_request" not in local_var_params or local_var_params["card_patch_request"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `card_patch_request` when calling `update`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "app_id" in local_var_params:
            path_params["appId"] = local_var_params["app_id"]  # noqa: E501
        if "card_id" in local_var_params:
            path_params["cardId"] = local_var_params["card_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "card_patch_request" in local_var_params:
            body_params = local_var_params["card_patch_request"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["developer_hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/crm/v3/extensions/cards/{appId}/{cardId}",
            "PATCH",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CardResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
