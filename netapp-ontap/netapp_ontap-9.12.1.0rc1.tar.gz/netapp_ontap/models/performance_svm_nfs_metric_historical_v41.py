r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["PerformanceSvmNfsMetricHistoricalV41", "PerformanceSvmNfsMetricHistoricalV41Schema"]
__pdoc__ = {
    "PerformanceSvmNfsMetricHistoricalV41Schema.resource": False,
    "PerformanceSvmNfsMetricHistoricalV41Schema.opts": False,
    "PerformanceSvmNfsMetricHistoricalV41": False,
}


class PerformanceSvmNfsMetricHistoricalV41Schema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the PerformanceSvmNfsMetricHistoricalV41 object"""

    duration = fields.Str(data_key="duration")
    r""" The duration over which this sample is calculated. The time durations are represented in the ISO-8601 standard format. Samples can be calculated over the following durations:


Valid choices:

* PT15S
* PT30M
* PT2H
* P1D
* PT5M """

    iops = fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", unknown=EXCLUDE, data_key="iops")
    r""" The iops field of the performance_svm_nfs_metric_historical_v41. """

    latency = fields.Nested("netapp_ontap.models.performance_metric_io_type.PerformanceMetricIoTypeSchema", unknown=EXCLUDE, data_key="latency")
    r""" The latency field of the performance_svm_nfs_metric_historical_v41. """

    status = fields.Str(data_key="status")
    r""" Any errors associated with the sample. For example, if the aggregation of data over multiple nodes fails then any of the partial errors might be returned, "ok" on success, or "error" on any internal uncategorized failure. Whenever a sample collection is missed but done at a later time, it is back filled to the previous 15 second timestamp and tagged with "backfilled_data". "Inconsistent_ delta_time" is encountered when the time between two collections is not the same for all nodes. Therefore, the aggregated value might be over or under inflated. "Negative_delta" is returned when an expected monotonically increasing value has decreased in value. "Inconsistent_old_data" is returned when one or more nodes do not have the latest data.

Valid choices:

* ok
* error
* partial_no_data
* partial_no_response
* partial_other_error
* negative_delta
* not_found
* backfilled_data
* inconsistent_delta_time
* inconsistent_old_data
* partial_no_uuid """

    throughput = fields.Nested("netapp_ontap.models.performance_metric_io_type_rwt.PerformanceMetricIoTypeRwtSchema", unknown=EXCLUDE, data_key="throughput")
    r""" The throughput field of the performance_svm_nfs_metric_historical_v41. """

    @property
    def resource(self):
        return PerformanceSvmNfsMetricHistoricalV41

    gettable_fields = [
        "duration",
        "iops.other",
        "iops.read",
        "iops.total",
        "iops.write",
        "latency.other",
        "latency.read",
        "latency.total",
        "latency.write",
        "status",
        "throughput.read",
        "throughput.total",
        "throughput.write",
    ]
    """duration,iops.other,iops.read,iops.total,iops.write,latency.other,latency.read,latency.total,latency.write,status,throughput.read,throughput.total,throughput.write,"""

    patchable_fields = [
        "iops.other",
        "iops.read",
        "iops.total",
        "iops.write",
        "latency.other",
        "latency.read",
        "latency.total",
        "latency.write",
        "throughput.read",
        "throughput.total",
        "throughput.write",
    ]
    """iops.other,iops.read,iops.total,iops.write,latency.other,latency.read,latency.total,latency.write,throughput.read,throughput.total,throughput.write,"""

    postable_fields = [
        "iops.other",
        "iops.read",
        "iops.total",
        "iops.write",
        "latency.other",
        "latency.read",
        "latency.total",
        "latency.write",
        "throughput.read",
        "throughput.total",
        "throughput.write",
    ]
    """iops.other,iops.read,iops.total,iops.write,latency.other,latency.read,latency.total,latency.write,throughput.read,throughput.total,throughput.write,"""


class PerformanceSvmNfsMetricHistoricalV41(Resource):

    _schema = PerformanceSvmNfsMetricHistoricalV41Schema
