r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["AppNfsAccess", "AppNfsAccessSchema"]
__pdoc__ = {
    "AppNfsAccessSchema.resource": False,
    "AppNfsAccessSchema.opts": False,
    "AppNfsAccess": False,
}


class AppNfsAccessSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the AppNfsAccess object"""

    access = fields.Str(data_key="access")
    r""" The NFS access granted.

Valid choices:

* none
* ro
* rw """

    host = fields.Str(data_key="host")
    r""" The name of the NFS entity granted access. """

    @property
    def resource(self):
        return AppNfsAccess

    gettable_fields = [
        "access",
        "host",
    ]
    """access,host,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "access",
        "host",
    ]
    """access,host,"""


class AppNfsAccess(Resource):

    _schema = AppNfsAccessSchema
