r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["DiskKeyId", "DiskKeyIdSchema"]
__pdoc__ = {
    "DiskKeyIdSchema.resource": False,
    "DiskKeyIdSchema.opts": False,
    "DiskKeyId": False,
}


class DiskKeyIdSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the DiskKeyId object"""

    data = fields.Str(data_key="data")
    r""" Key ID of the data authentication key """

    fips = fields.Str(data_key="fips")
    r""" Key ID of the FIPS authentication key """

    @property
    def resource(self):
        return DiskKeyId

    gettable_fields = [
        "data",
        "fips",
    ]
    """data,fips,"""

    patchable_fields = [
        "data",
        "fips",
    ]
    """data,fips,"""

    postable_fields = [
        "data",
        "fips",
    ]
    """data,fips,"""


class DiskKeyId(Resource):

    _schema = DiskKeyIdSchema
