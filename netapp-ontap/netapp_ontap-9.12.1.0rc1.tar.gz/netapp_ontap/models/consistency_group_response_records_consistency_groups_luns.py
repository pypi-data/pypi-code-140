r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupResponseRecordsConsistencyGroupsLuns", "ConsistencyGroupResponseRecordsConsistencyGroupsLunsSchema"]
__pdoc__ = {
    "ConsistencyGroupResponseRecordsConsistencyGroupsLunsSchema.resource": False,
    "ConsistencyGroupResponseRecordsConsistencyGroupsLunsSchema.opts": False,
    "ConsistencyGroupResponseRecordsConsistencyGroupsLuns": False,
}


class ConsistencyGroupResponseRecordsConsistencyGroupsLunsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupResponseRecordsConsistencyGroupsLuns object"""

    clone = fields.Nested("netapp_ontap.models.consistency_group_consistency_groups_luns_clone.ConsistencyGroupConsistencyGroupsLunsCloneSchema", unknown=EXCLUDE, data_key="clone")
    r""" The clone field of the consistency_group_response_records_consistency_groups_luns. """

    comment = fields.Str(data_key="comment")
    r""" A configurable comment available for use by the administrator. Valid in POST and PATCH. """

    create_time = ImpreciseDateTime(data_key="create_time")
    r""" The time the LUN was created.

Example: 2018-06-04T19:00:00Z """

    enabled = fields.Boolean(data_key="enabled")
    r""" The enabled state of the LUN. LUNs can be disabled to prevent access to the LUN. Certain error conditions also cause the LUN to become disabled. If the LUN is disabled, you can consult the `state` property to determine if the LUN is administratively disabled (_offline_) or has become disabled as a result of an error. A LUN in an error condition can be brought online by setting the `enabled` property to _true_ or brought administratively offline by setting the `enabled` property to _false_. Upon creation, a LUN is enabled by default. Valid in PATCH. """

    lun_maps = fields.List(fields.Nested("netapp_ontap.models.consistency_group_lun_lun_maps.ConsistencyGroupLunLunMapsSchema", unknown=EXCLUDE), data_key="lun_maps")
    r""" An array of LUN maps.<br/>
A LUN map is an association between a LUN and an initiator group. When a LUN is mapped to an initiator group, the initiator group's initiators are granted access to the LUN. The relationship between a LUN and an initiator group is many LUNs to many initiator groups. """

    name = fields.Str(data_key="name")
    r""" The fully qualified path name of the LUN composed of the "/vol" prefix, the volume name, the qtree name (optional), and the base name of the LUN. Valid in POST and PATCH.


Example: /vol/volume1/lun1 """

    os_type = fields.Str(data_key="os_type")
    r""" The operating system type of the LUN.<br/>
Required in POST when creating a LUN that is not a clone of another. Disallowed in POST when creating a LUN clone.


Valid choices:

* aix
* hpux
* hyper_v
* linux
* netware
* openvms
* solaris
* solaris_efi
* vmware
* windows
* windows_2008
* windows_gpt
* xen """

    provisioning_options = fields.Nested("netapp_ontap.models.consistency_group_vdisk_provisioning_options.ConsistencyGroupVdiskProvisioningOptionsSchema", unknown=EXCLUDE, data_key="provisioning_options")
    r""" The provisioning_options field of the consistency_group_response_records_consistency_groups_luns. """

    qos = fields.Nested("netapp_ontap.models.consistency_group_qos.ConsistencyGroupQosSchema", unknown=EXCLUDE, data_key="qos")
    r""" The qos field of the consistency_group_response_records_consistency_groups_luns. """

    serial_number = fields.Str(data_key="serial_number")
    r""" The LUN serial number. The serial number is generated by ONTAP when the LUN is created. """

    space = fields.Nested("netapp_ontap.models.consistency_group_lun_space.ConsistencyGroupLunSpaceSchema", unknown=EXCLUDE, data_key="space")
    r""" The space field of the consistency_group_response_records_consistency_groups_luns. """

    uuid = fields.Str(data_key="uuid")
    r""" The unique identifier of the LUN.  The UUID is generated by ONTAP when the LUN is created.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return ConsistencyGroupResponseRecordsConsistencyGroupsLuns

    gettable_fields = [
        "comment",
        "create_time",
        "enabled",
        "lun_maps",
        "name",
        "os_type",
        "qos.policy",
        "serial_number",
        "space",
        "uuid",
    ]
    """comment,create_time,enabled,lun_maps,name,os_type,qos.policy,serial_number,space,uuid,"""

    patchable_fields = [
        "clone",
        "comment",
        "lun_maps",
        "provisioning_options",
        "qos.policy",
        "space",
    ]
    """clone,comment,lun_maps,provisioning_options,qos.policy,space,"""

    postable_fields = [
        "clone",
        "comment",
        "lun_maps",
        "name",
        "os_type",
        "provisioning_options",
        "qos.policy",
        "space",
    ]
    """clone,comment,lun_maps,name,os_type,provisioning_options,qos.policy,space,"""


class ConsistencyGroupResponseRecordsConsistencyGroupsLuns(Resource):

    _schema = ConsistencyGroupResponseRecordsConsistencyGroupsLunsSchema
