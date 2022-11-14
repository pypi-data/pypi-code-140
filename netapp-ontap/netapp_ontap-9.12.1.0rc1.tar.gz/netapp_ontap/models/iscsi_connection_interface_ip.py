r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["IscsiConnectionInterfaceIp", "IscsiConnectionInterfaceIpSchema"]
__pdoc__ = {
    "IscsiConnectionInterfaceIpSchema.resource": False,
    "IscsiConnectionInterfaceIpSchema.opts": False,
    "IscsiConnectionInterfaceIp": False,
}


class IscsiConnectionInterfaceIpSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the IscsiConnectionInterfaceIp object"""

    address = fields.Str(data_key="address")
    r""" The address field of the iscsi_connection_interface_ip. """

    port = Size(data_key="port")
    r""" The TCP port number of the iSCSI access endpoint.

Example: 3260 """

    @property
    def resource(self):
        return IscsiConnectionInterfaceIp

    gettable_fields = [
        "address",
        "port",
    ]
    """address,port,"""

    patchable_fields = [
        "address",
    ]
    """address,"""

    postable_fields = [
        "address",
    ]
    """address,"""


class IscsiConnectionInterfaceIp(Resource):

    _schema = IscsiConnectionInterfaceIpSchema
