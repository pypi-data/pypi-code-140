r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityKeyManagerExternalServerCaCertificates", "SecurityKeyManagerExternalServerCaCertificatesSchema"]
__pdoc__ = {
    "SecurityKeyManagerExternalServerCaCertificatesSchema.resource": False,
    "SecurityKeyManagerExternalServerCaCertificatesSchema.opts": False,
    "SecurityKeyManagerExternalServerCaCertificates": False,
}


class SecurityKeyManagerExternalServerCaCertificatesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeyManagerExternalServerCaCertificates object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the security_key_manager_external_server_ca_certificates. """

    uuid = fields.Str(data_key="uuid")
    r""" Certificate UUID

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return SecurityKeyManagerExternalServerCaCertificates

    gettable_fields = [
        "links",
        "uuid",
    ]
    """links,uuid,"""

    patchable_fields = [
        "uuid",
    ]
    """uuid,"""

    postable_fields = [
        "uuid",
    ]
    """uuid,"""


class SecurityKeyManagerExternalServerCaCertificates(Resource):

    _schema = SecurityKeyManagerExternalServerCaCertificatesSchema
