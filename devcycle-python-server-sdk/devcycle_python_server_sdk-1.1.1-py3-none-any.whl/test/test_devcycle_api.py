# coding: utf-8

"""
    DevCycle Bucketing API

    Documents the DevCycle Bucketing API which provides and API interface to User Bucketing and for generated SDKs.  # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import devcycle_python_sdk
from devcycle_python_sdk.api.devcycle_api import DevcycleApi  # noqa: E501
from devcycle_python_sdk.rest import ApiException


class TestDevcycleApi(unittest.TestCase):
    """DevcycleApi unit test stubs"""

    def setUp(self):
        self.api = DevcycleApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_features(self):
        """Test case for get_features

        Get all features by key for user data  # noqa: E501
        """
        pass

    def test_get_variable_by_key(self):
        """Test case for get_variable_by_key

        Get variable by key for user data  # noqa: E501
        """
        pass

    def test_get_variables(self):
        """Test case for get_variables

        Get all variables by key for user data  # noqa: E501
        """
        pass

    def test_post_events(self):
        """Test case for post_events

        Post events to DevCycle for user  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
