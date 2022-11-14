# coding: utf-8

"""
    Subscriptions

    Subscriptions allow contacts to control what forms of communications they receive. Contacts can decide whether they want to receive communication pertaining to a specific topic, brand, or an entire HubSpot account.  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from hubspot.communication_preferences.api_client import ApiClient
from hubspot.communication_preferences.exceptions import ApiTypeError, ApiValueError


class StatusApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_email_status(self, email_address, **kwargs):  # noqa: E501
        """Get subscription statuses for a contact  # noqa: E501

        Returns a list of subscriptions and their status for a given contact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_email_status(email_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str email_address: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PublicSubscriptionStatusesResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_email_status_with_http_info(email_address, **kwargs)  # noqa: E501

    def get_email_status_with_http_info(self, email_address, **kwargs):  # noqa: E501
        """Get subscription statuses for a contact  # noqa: E501

        Returns a list of subscriptions and their status for a given contact.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_email_status_with_http_info(email_address, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str email_address: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PublicSubscriptionStatusesResponse, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["email_address"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method get_email_status" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'email_address' is set
        if self.api_client.client_side_validation and ("email_address" not in local_var_params or local_var_params["email_address"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `email_address` when calling `get_email_status`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "email_address" in local_var_params:
            path_params["emailAddress"] = local_var_params["email_address"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/communication-preferences/v3/status/email/{emailAddress}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="PublicSubscriptionStatusesResponse",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def subscribe(self, public_update_subscription_status_request, **kwargs):  # noqa: E501
        """Subscribe a contact  # noqa: E501

        Subscribes a contact to the given subscription type. This API is not valid to use for subscribing a contact at a brand or portal level and will return an error.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.subscribe(public_update_subscription_status_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param PublicUpdateSubscriptionStatusRequest public_update_subscription_status_request: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PublicSubscriptionStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.subscribe_with_http_info(public_update_subscription_status_request, **kwargs)  # noqa: E501

    def subscribe_with_http_info(self, public_update_subscription_status_request, **kwargs):  # noqa: E501
        """Subscribe a contact  # noqa: E501

        Subscribes a contact to the given subscription type. This API is not valid to use for subscribing a contact at a brand or portal level and will return an error.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.subscribe_with_http_info(public_update_subscription_status_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param PublicUpdateSubscriptionStatusRequest public_update_subscription_status_request: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PublicSubscriptionStatus, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["public_update_subscription_status_request"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method subscribe" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'public_update_subscription_status_request' is set
        if self.api_client.client_side_validation and (
            "public_update_subscription_status_request" not in local_var_params or local_var_params["public_update_subscription_status_request"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `public_update_subscription_status_request` when calling `subscribe`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "public_update_subscription_status_request" in local_var_params:
            body_params = local_var_params["public_update_subscription_status_request"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/communication-preferences/v3/subscribe",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="PublicSubscriptionStatus",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def unsubscribe(self, public_update_subscription_status_request, **kwargs):  # noqa: E501
        """Unsubscribe a contact  # noqa: E501

        Unsubscribes a contact from the given subscription type. This API is not valid to use for unsubscribing a contact at a brand or portal level and will return an error.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsubscribe(public_update_subscription_status_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param PublicUpdateSubscriptionStatusRequest public_update_subscription_status_request: (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: PublicSubscriptionStatus
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.unsubscribe_with_http_info(public_update_subscription_status_request, **kwargs)  # noqa: E501

    def unsubscribe_with_http_info(self, public_update_subscription_status_request, **kwargs):  # noqa: E501
        """Unsubscribe a contact  # noqa: E501

        Unsubscribes a contact from the given subscription type. This API is not valid to use for unsubscribing a contact at a brand or portal level and will return an error.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.unsubscribe_with_http_info(public_update_subscription_status_request, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param PublicUpdateSubscriptionStatusRequest public_update_subscription_status_request: (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(PublicSubscriptionStatus, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["public_update_subscription_status_request"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method unsubscribe" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'public_update_subscription_status_request' is set
        if self.api_client.client_side_validation and (
            "public_update_subscription_status_request" not in local_var_params or local_var_params["public_update_subscription_status_request"] is None  # noqa: E501
        ):  # noqa: E501
            raise ApiValueError("Missing the required parameter `public_update_subscription_status_request` when calling `unsubscribe`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if "public_update_subscription_status_request" in local_var_params:
            body_params = local_var_params["public_update_subscription_status_request"]
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # HTTP header `Content-Type`
        header_params["Content-Type"] = self.api_client.select_header_content_type(["application/json"])  # noqa: E501  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey", "oauth2"]  # noqa: E501

        return self.api_client.call_api(
            "/communication-preferences/v3/unsubscribe",
            "POST",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="PublicSubscriptionStatus",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
