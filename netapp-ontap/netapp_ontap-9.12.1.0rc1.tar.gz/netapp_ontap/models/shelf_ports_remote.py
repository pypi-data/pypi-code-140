r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ShelfPortsRemote", "ShelfPortsRemoteSchema"]
__pdoc__ = {
    "ShelfPortsRemoteSchema.resource": False,
    "ShelfPortsRemoteSchema.opts": False,
    "ShelfPortsRemote": False,
}


class ShelfPortsRemoteSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ShelfPortsRemote object"""

    chassis = fields.Str(data_key="chassis")
    r""" The chassis field of the shelf_ports_remote. """

    device = fields.Str(data_key="device")
    r""" The device field of the shelf_ports_remote. """

    mac_address = fields.Str(data_key="mac_address")
    r""" The mac_address field of the shelf_ports_remote. """

    phy = fields.Str(data_key="phy")
    r""" The phy field of the shelf_ports_remote.

Example: 12 """

    port = fields.Str(data_key="port")
    r""" The port field of the shelf_ports_remote. """

    wwn = fields.Str(data_key="wwn")
    r""" The wwn field of the shelf_ports_remote.

Example: 50000D1703544B80 """

    @property
    def resource(self):
        return ShelfPortsRemote

    gettable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""

    patchable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""

    postable_fields = [
        "chassis",
        "device",
        "mac_address",
        "phy",
        "port",
        "wwn",
    ]
    """chassis,device,mac_address,phy,port,wwn,"""


class ShelfPortsRemote(Resource):

    _schema = ShelfPortsRemoteSchema
