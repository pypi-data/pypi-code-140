r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NetworkRouteInterfaces", "NetworkRouteInterfacesSchema"]
__pdoc__ = {
    "NetworkRouteInterfacesSchema.resource": False,
    "NetworkRouteInterfacesSchema.opts": False,
    "NetworkRouteInterfaces": False,
}


class NetworkRouteInterfacesSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NetworkRouteInterfaces object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the network_route_interfaces. """

    ip = fields.Nested("netapp_ontap.models.application_san_access_iscsi_endpoint_interface_ip.ApplicationSanAccessIscsiEndpointInterfaceIpSchema", unknown=EXCLUDE, data_key="ip")
    r""" The ip field of the network_route_interfaces. """

    name = fields.Str(data_key="name")
    r""" The name of the interface. If only the name is provided, the SVM scope
must be provided by the object this object is embedded in.


Example: lif1 """

    uuid = fields.Str(data_key="uuid")
    r""" The UUID that uniquely identifies the interface.

Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return NetworkRouteInterfaces

    gettable_fields = [
        "links",
        "ip",
        "name",
        "uuid",
    ]
    """links,ip,name,uuid,"""

    patchable_fields = [
        "ip",
        "name",
        "uuid",
    ]
    """ip,name,uuid,"""

    postable_fields = [
        "ip",
        "name",
        "uuid",
    ]
    """ip,name,uuid,"""


class NetworkRouteInterfaces(Resource):

    _schema = NetworkRouteInterfacesSchema
