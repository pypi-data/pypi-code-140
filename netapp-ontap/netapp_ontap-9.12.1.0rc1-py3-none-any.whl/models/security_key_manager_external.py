r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["SecurityKeyManagerExternal", "SecurityKeyManagerExternalSchema"]
__pdoc__ = {
    "SecurityKeyManagerExternalSchema.resource": False,
    "SecurityKeyManagerExternalSchema.opts": False,
    "SecurityKeyManagerExternal": False,
}


class SecurityKeyManagerExternalSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the SecurityKeyManagerExternal object"""

    client_certificate = fields.Nested("netapp_ontap.models.security_certificate_ref_uuid.SecurityCertificateRefUuidSchema", unknown=EXCLUDE, data_key="client_certificate")
    r""" The client_certificate field of the security_key_manager_external. """

    server_ca_certificates = fields.List(fields.Nested("netapp_ontap.models.security_certificate_ref_uuid.SecurityCertificateRefUuidSchema", unknown=EXCLUDE), data_key="server_ca_certificates")
    r""" The UUIDs of the server CA certificates already installed in the cluster or SVM. The array of certificates are common for all the keyservers per SVM. """

    servers = fields.List(fields.Nested("netapp_ontap.models.key_server_readcreate.KeyServerReadcreateSchema", unknown=EXCLUDE), data_key="servers")
    r""" The set of external key servers. """

    @property
    def resource(self):
        return SecurityKeyManagerExternal

    gettable_fields = [
        "client_certificate",
        "server_ca_certificates",
        "servers",
    ]
    """client_certificate,server_ca_certificates,servers,"""

    patchable_fields = [
        "client_certificate",
        "server_ca_certificates",
        "servers",
    ]
    """client_certificate,server_ca_certificates,servers,"""

    postable_fields = [
        "client_certificate",
        "server_ca_certificates",
        "servers",
    ]
    """client_certificate,server_ca_certificates,servers,"""


class SecurityKeyManagerExternal(Resource):

    _schema = SecurityKeyManagerExternalSchema
