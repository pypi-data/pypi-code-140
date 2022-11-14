r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupResponseRecordsConsistencyGroups", "ConsistencyGroupResponseRecordsConsistencyGroupsSchema"]
__pdoc__ = {
    "ConsistencyGroupResponseRecordsConsistencyGroupsSchema.resource": False,
    "ConsistencyGroupResponseRecordsConsistencyGroupsSchema.opts": False,
    "ConsistencyGroupResponseRecordsConsistencyGroups": False,
}


class ConsistencyGroupResponseRecordsConsistencyGroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupResponseRecordsConsistencyGroups object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the consistency_group_response_records_consistency_groups. """

    application = fields.Nested("netapp_ontap.models.consistency_group_application.ConsistencyGroupApplicationSchema", unknown=EXCLUDE, data_key="application")
    r""" The application field of the consistency_group_response_records_consistency_groups. """

    luns = fields.List(fields.Nested("netapp_ontap.models.consistency_group_lun.ConsistencyGroupLunSchema", unknown=EXCLUDE), data_key="luns")
    r""" The LUNs array can be used to create or modify LUNs in a consistency group on a new or existing volume that is a member of the consistency group. LUNs are considered members of a consistency group if they are located on a volume that is a member of the consistency group. """

    name = fields.Str(data_key="name")
    r""" Name of the consistency group. The consistency group name must be unique within an SVM.<br/>
If not provided and the consistency group contains only one volume, the name will be generated based on the volume name. If the consistency group contains more than one volume, the name is required. """

    namespaces = fields.List(fields.Nested("netapp_ontap.models.consistency_group_child_namespaces.ConsistencyGroupChildNamespacesSchema", unknown=EXCLUDE), data_key="namespaces")
    r""" An NVMe namespace is a collection of addressable logical blocks presented to hosts connected to the SVM using the NVMe over Fabrics protocol.
In ONTAP, an NVMe namespace is located within a volume. Optionally, it can be located within a qtree in a volume.<br/>
An NVMe namespace is created to a specified size using thin or thick provisioning as determined by the volume on which it is created. NVMe namespaces support being cloned. An NVMe namespace cannot be renamed, resized, or moved to a different volume. NVMe namespaces do not support the assignment of a QoS policy for performance management, but a QoS policy can be assigned to the volume containing the namespace. See the NVMe namespace object model to learn more about each of the properties supported by the NVMe namespace REST API.<br/>
An NVMe namespace must be mapped to an NVMe subsystem to grant access to the subsystem's hosts. Hosts can then access the NVMe namespace and perform I/O using the NVMe over Fabrics protocol. """

    parent_consistency_group = fields.Nested("netapp_ontap.resources.consistency_group.ConsistencyGroupSchema", unknown=EXCLUDE, data_key="parent_consistency_group")
    r""" The parent_consistency_group field of the consistency_group_response_records_consistency_groups. """

    provisioning_options = fields.Nested("netapp_ontap.models.consistency_group_provisioning_options.ConsistencyGroupProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options")
    r""" The provisioning_options field of the consistency_group_response_records_consistency_groups. """

    qos = fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos")
    r""" The qos field of the consistency_group_response_records_consistency_groups. """

    restore_to = fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_restore_to.ConsistencyGroupConsistencyGroupsRestoreToSchema", unknown=EXCLUDE, data_key="restore_to")
    r""" The restore_to field of the consistency_group_response_records_consistency_groups. """

    snapshot_policy = fields.Nested("netapp_ontap.resources.snapshot_policy.SnapshotPolicySchema", unknown=EXCLUDE, data_key="snapshot_policy")
    r""" The Snapshot copy policy of the consistency group.<br/>
This is the dedicated consistency group Snapshot copy policy, not an aggregation of the volume granular Snapshot copy policy. """

    space = fields.Nested("netapp_ontap.models.consistency_group_space.ConsistencyGroupSpaceSchema", unknown=EXCLUDE, data_key="space")
    r""" The space field of the consistency_group_response_records_consistency_groups. """

    svm = fields.Nested("netapp_ontap.resources.svm.SvmSchema", unknown=EXCLUDE, data_key="svm")
    r""" The svm field of the consistency_group_response_records_consistency_groups. """

    tiering = fields.Nested("netapp_ontap.models.consistency_group_tiering.ConsistencyGroupTieringSchema", unknown=EXCLUDE, data_key="tiering")
    r""" The tiering field of the consistency_group_response_records_consistency_groups. """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the consistency group. The UUID is generated by ONTAP when the consistency group is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    volumes = fields.List(fields.Nested("netapp_ontap.models.consistency_group_child_volumes.ConsistencyGroupChildVolumesSchema", unknown=EXCLUDE), data_key="volumes")
    r""" A consistency group is a mutually exclusive aggregation of volumes or other consistency groups. A volume can only be associated with one direct parent consistency group.<br/>
The volumes array can be used to create new volumes in the consistency group, add existing volumes to the consistency group, or modify existing volumes that are already members of the consistency group.<br/>
The total number of volumes across all child consistency groups contained in a consistency group is constrained by the same limit. """

    @property
    def resource(self):
        return ConsistencyGroupResponseRecordsConsistencyGroups

    gettable_fields = [
        "links",
        "application",
        "luns",
        "name",
        "namespaces",
        "parent_consistency_group.links",
        "parent_consistency_group.name",
        "parent_consistency_group.uuid",
        "qos",
        "snapshot_policy.links",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "space",
        "svm.links",
        "svm.name",
        "svm.uuid",
        "tiering",
        "uuid",
        "volumes",
    ]
    """links,application,luns,name,namespaces,parent_consistency_group.links,parent_consistency_group.name,parent_consistency_group.uuid,qos,snapshot_policy.links,snapshot_policy.name,snapshot_policy.uuid,space,svm.links,svm.name,svm.uuid,tiering,uuid,volumes,"""

    patchable_fields = [
        "application",
        "luns",
        "namespaces",
        "provisioning_options",
        "qos",
        "restore_to",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "volumes",
    ]
    """application,luns,namespaces,provisioning_options,qos,restore_to,snapshot_policy.name,snapshot_policy.uuid,volumes,"""

    postable_fields = [
        "application",
        "luns",
        "name",
        "namespaces",
        "provisioning_options",
        "qos",
        "snapshot_policy.name",
        "snapshot_policy.uuid",
        "svm.name",
        "svm.uuid",
        "tiering",
        "volumes",
    ]
    """application,luns,name,namespaces,provisioning_options,qos,snapshot_policy.name,snapshot_policy.uuid,svm.name,svm.uuid,tiering,volumes,"""


class ConsistencyGroupResponseRecordsConsistencyGroups(Resource):

    _schema = ConsistencyGroupResponseRecordsConsistencyGroupsSchema
