r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AggregateSpace", "AggregateSpaceSchema"]
__pdoc__ = {
    "AggregateSpaceSchema.resource": False,
    "AggregateSpaceSchema.opts": False,
    "AggregateSpace": False,
}


class AggregateSpaceSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AggregateSpace object"""

    block_storage = fields.Nested("netapp_ontap.models.aggregate_space_block_storage.AggregateSpaceBlockStorageSchema", unknown=EXCLUDE, data_key="block_storage")
    r""" The block_storage field of the aggregate_space. """

    cloud_storage = fields.Nested("netapp_ontap.models.aggregate_space_cloud_storage.AggregateSpaceCloudStorageSchema", unknown=EXCLUDE, data_key="cloud_storage")
    r""" The cloud_storage field of the aggregate_space. """

    efficiency = fields.Nested("netapp_ontap.models.aggr_space_efficiency.AggrSpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency")
    r""" The efficiency field of the aggregate_space. """

    efficiency_without_snapshots = fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency_without_snapshots")
    r""" The efficiency_without_snapshots field of the aggregate_space. """

    efficiency_without_snapshots_flexclones = fields.Nested("netapp_ontap.models.space_efficiency.SpaceEfficiencySchema", unknown=EXCLUDE, data_key="efficiency_without_snapshots_flexclones")
    r""" The efficiency_without_snapshots_flexclones field of the aggregate_space. """

    footprint = Size(data_key="footprint")
    r""" A summation of volume footprints (including volume guarantees), in bytes. This includes all of the volume footprints in the block_storage tier and the cloud_storage tier.
This is an advanced property; there is an added computational cost to retrieving its value. The field is not populated for either a collection GET or an instance GET unless it is explicitly requested using the <i>fields</i> query parameter containing either footprint or **.


Example: 608896 """

    snapshot = fields.Nested("netapp_ontap.models.aggregate_space_snapshot.AggregateSpaceSnapshotSchema", unknown=EXCLUDE, data_key="snapshot")
    r""" The snapshot field of the aggregate_space. """

    @property
    def resource(self):
        return AggregateSpace

    gettable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "footprint",
        "snapshot",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,footprint,snapshot,"""

    patchable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "snapshot",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,snapshot,"""

    postable_fields = [
        "block_storage",
        "cloud_storage",
        "efficiency",
        "efficiency_without_snapshots",
        "efficiency_without_snapshots_flexclones",
        "snapshot",
    ]
    """block_storage,cloud_storage,efficiency,efficiency_without_snapshots,efficiency_without_snapshots_flexclones,snapshot,"""


class AggregateSpace(Resource):

    _schema = AggregateSpaceSchema
