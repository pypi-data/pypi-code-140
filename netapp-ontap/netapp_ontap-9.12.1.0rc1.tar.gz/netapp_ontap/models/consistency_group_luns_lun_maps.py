r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupLunsLunMaps", "ConsistencyGroupLunsLunMapsSchema"]
__pdoc__ = {
    "ConsistencyGroupLunsLunMapsSchema.resource": False,
    "ConsistencyGroupLunsLunMapsSchema.opts": False,
    "ConsistencyGroupLunsLunMaps": False,
}


class ConsistencyGroupLunsLunMapsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupLunsLunMaps object"""

    igroup = fields.Nested("netapp_ontap.models.consistency_group_igroup.ConsistencyGroupIgroupSchema", unknown=EXCLUDE, data_key="igroup")
    r""" The igroup field of the consistency_group_luns_lun_maps. """

    logical_unit_number = Size(data_key="logical_unit_number")
    r""" The logical unit number assigned to the LUN when mapped to the specified initiator group. The number is used to identify the LUN to initiators in the initiator group when communicating through the Fibre Channel Protocol or iSCSI. Optional in POST; if no value is provided, ONTAP assigns the lowest available value. """

    @property
    def resource(self):
        return ConsistencyGroupLunsLunMaps

    gettable_fields = [
        "igroup",
        "logical_unit_number",
    ]
    """igroup,logical_unit_number,"""

    patchable_fields = [
        "igroup",
    ]
    """igroup,"""

    postable_fields = [
        "igroup",
        "logical_unit_number",
    ]
    """igroup,logical_unit_number,"""


class ConsistencyGroupLunsLunMaps(Resource):

    _schema = ConsistencyGroupLunsLunMapsSchema
