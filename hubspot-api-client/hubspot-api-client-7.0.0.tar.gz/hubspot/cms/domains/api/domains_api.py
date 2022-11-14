# coding: utf-8

"""
    Domains

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from hubspot.cms.domains.api_client import ApiClient
from hubspot.cms.domains.exceptions import ApiTypeError, ApiValueError


class DomainsApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_by_id(self, domain_id, **kwargs):  # noqa: E501
        """Get a single domain  # noqa: E501

        Returns a single domains with the id specified.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_by_id(domain_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str domain_id: The unique ID of the domain. (required)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: Domain
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_by_id_with_http_info(domain_id, **kwargs)  # noqa: E501

    def get_by_id_with_http_info(self, domain_id, **kwargs):  # noqa: E501
        """Get a single domain  # noqa: E501

        Returns a single domains with the id specified.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_by_id_with_http_info(domain_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str domain_id: The unique ID of the domain. (required)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(Domain, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["domain_id"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method get_by_id" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]
        # verify the required parameter 'domain_id' is set
        if self.api_client.client_side_validation and ("domain_id" not in local_var_params or local_var_params["domain_id"] is None):  # noqa: E501  # noqa: E501
            raise ApiValueError("Missing the required parameter `domain_id` when calling `get_by_id`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if "domain_id" in local_var_params:
            path_params["domainId"] = local_var_params["domain_id"]  # noqa: E501

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/cms/v3/domains/{domainId}",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="Domain",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )

    def get_page(self, **kwargs):  # noqa: E501
        """Get current domains  # noqa: E501

        Returns all existing domains that have been created. Results can be limited and filtered by creation or updated date.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_page(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param datetime created_at: Only return domains created at this date.
        :param datetime created_after: Only return domains created after this date.
        :param datetime created_before: Only return domains created before this date.
        :param datetime updated_at: Only return domains updated at this date.
        :param datetime updated_after: Only return domains updated after this date.
        :param datetime updated_before: Only return domains updated before this date.
        :param list[str] sort:
        :param str after: The paging cursor token of the last successfully read resource will be returned as the `paging.next.after` JSON property of a paged response containing more results.
        :param int limit: Maximum number of results per page.
        :param bool archived: Whether to return only results that have been archived.
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: CollectionResponseWithTotalDomainForwardPaging
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs["_return_http_data_only"] = True
        return self.get_page_with_http_info(**kwargs)  # noqa: E501

    def get_page_with_http_info(self, **kwargs):  # noqa: E501
        """Get current domains  # noqa: E501

        Returns all existing domains that have been created. Results can be limited and filtered by creation or updated date.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_page_with_http_info(async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param datetime created_at: Only return domains created at this date.
        :param datetime created_after: Only return domains created after this date.
        :param datetime created_before: Only return domains created before this date.
        :param datetime updated_at: Only return domains updated at this date.
        :param datetime updated_after: Only return domains updated after this date.
        :param datetime updated_before: Only return domains updated before this date.
        :param list[str] sort:
        :param str after: The paging cursor token of the last successfully read resource will be returned as the `paging.next.after` JSON property of a paged response containing more results.
        :param int limit: Maximum number of results per page.
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
        :return: tuple(CollectionResponseWithTotalDomainForwardPaging, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ["created_at", "created_after", "created_before", "updated_at", "updated_after", "updated_before", "sort", "after", "limit", "archived"]  # noqa: E501
        all_params.append("async_req")
        all_params.append("_return_http_data_only")
        all_params.append("_preload_content")
        all_params.append("_request_timeout")

        for key, val in six.iteritems(local_var_params["kwargs"]):
            if key not in all_params:
                raise ApiTypeError("Got an unexpected keyword argument '%s'" " to method get_page" % key)
            local_var_params[key] = val
        del local_var_params["kwargs"]

        collection_formats = {}

        path_params = {}

        query_params = []
        if "created_at" in local_var_params and local_var_params["created_at"] is not None:  # noqa: E501
            query_params.append(("createdAt", local_var_params["created_at"]))  # noqa: E501
        if "created_after" in local_var_params and local_var_params["created_after"] is not None:  # noqa: E501
            query_params.append(("createdAfter", local_var_params["created_after"]))  # noqa: E501
        if "created_before" in local_var_params and local_var_params["created_before"] is not None:  # noqa: E501
            query_params.append(("createdBefore", local_var_params["created_before"]))  # noqa: E501
        if "updated_at" in local_var_params and local_var_params["updated_at"] is not None:  # noqa: E501
            query_params.append(("updatedAt", local_var_params["updated_at"]))  # noqa: E501
        if "updated_after" in local_var_params and local_var_params["updated_after"] is not None:  # noqa: E501
            query_params.append(("updatedAfter", local_var_params["updated_after"]))  # noqa: E501
        if "updated_before" in local_var_params and local_var_params["updated_before"] is not None:  # noqa: E501
            query_params.append(("updatedBefore", local_var_params["updated_before"]))  # noqa: E501
        if "sort" in local_var_params and local_var_params["sort"] is not None:  # noqa: E501
            query_params.append(("sort", local_var_params["sort"]))  # noqa: E501
            collection_formats["sort"] = "multi"  # noqa: E501
        if "after" in local_var_params and local_var_params["after"] is not None:  # noqa: E501
            query_params.append(("after", local_var_params["after"]))  # noqa: E501
        if "limit" in local_var_params and local_var_params["limit"] is not None:  # noqa: E501
            query_params.append(("limit", local_var_params["limit"]))  # noqa: E501
        if "archived" in local_var_params and local_var_params["archived"] is not None:  # noqa: E501
            query_params.append(("archived", local_var_params["archived"]))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params["Accept"] = self.api_client.select_header_accept(["application/json", "*/*"])  # noqa: E501

        # Authentication setting
        auth_settings = ["hapikey"]  # noqa: E501

        return self.api_client.call_api(
            "/cms/v3/domains/",
            "GET",
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type="CollectionResponseWithTotalDomainForwardPaging",  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get("async_req"),
            _return_http_data_only=local_var_params.get("_return_http_data_only"),  # noqa: E501
            _preload_content=local_var_params.get("_preload_content", True),
            _request_timeout=local_var_params.get("_request_timeout"),
            collection_formats=collection_formats,
        )
