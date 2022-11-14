r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ClusterPeerSetup", "ClusterPeerSetupSchema"]
__pdoc__ = {
    "ClusterPeerSetupSchema.resource": False,
    "ClusterPeerSetupSchema.opts": False,
    "ClusterPeerSetup": False,
}


class ClusterPeerSetupSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ClusterPeerSetup object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the cluster_peer_setup. """

    authentication = fields.Nested("netapp_ontap.models.cluster_peer_setup_response_authentication.ClusterPeerSetupResponseAuthenticationSchema", unknown=EXCLUDE, data_key="authentication")
    r""" The authentication field of the cluster_peer_setup. """

    ip_address = fields.Str(data_key="ip_address")
    r""" A local intercluster IP address that a remote cluster can use, together with the passphrase, to create a cluster peer relationship with the local cluster. """

    name = fields.Str(data_key="name")
    r""" Optional name for the cluster peer relationship. By default, it is the name of the remote cluster, or a temporary name might be autogenerated for anonymous cluster peer offers.

Example: cluster2 """

    @property
    def resource(self):
        return ClusterPeerSetup

    gettable_fields = [
        "links",
        "authentication",
        "ip_address",
        "name",
    ]
    """links,authentication,ip_address,name,"""

    patchable_fields = [
        "authentication",
        "ip_address",
        "name",
    ]
    """authentication,ip_address,name,"""

    postable_fields = [
        "authentication",
        "ip_address",
        "name",
    ]
    """authentication,ip_address,name,"""


class ClusterPeerSetup(Resource):

    _schema = ClusterPeerSetupSchema
