# coding: utf-8

"""
    Data Repository API

    <details><summary>This document defines the REST API for the Terra Data Repository.</summary> <p> **Status: design in progress** There are a few top-level endpoints (besides some used by swagger):  * / - generated by swagger: swagger API page that provides this documentation and a live UI for submitting REST requests  * /status - provides the operational status of the service  * /configuration - provides the basic configuration and information about the service  * /api - is the authenticated and authorized Data Repository API  * /ga4gh/drs/v1 - is a transcription of the Data Repository Service API  The API endpoints are organized by interface. Each interface is separately versioned. <p> **Notes on Naming** <p> All of the reference items are suffixed with \\\"Model\\\". Those names are used as the class names in the generated Java code. It is helpful to distinguish these model classes from other related classes, like the DAO classes and the operation classes. </details>   # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import data_repo_client
from data_repo_client.api.journal_api import JournalApi  # noqa: E501
from data_repo_client.rest import ApiException


class TestJournalApi(unittest.TestCase):
    """JournalApi unit test stubs"""

    def setUp(self):
        self.api = data_repo_client.api.journal_api.JournalApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_retrieve_journal_entries(self):
        """Test case for retrieve_journal_entries

        """
        pass


if __name__ == '__main__':
    unittest.main()
