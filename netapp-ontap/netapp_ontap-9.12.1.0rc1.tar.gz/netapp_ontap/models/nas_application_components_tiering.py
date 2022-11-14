r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["NasApplicationComponentsTiering", "NasApplicationComponentsTieringSchema"]
__pdoc__ = {
    "NasApplicationComponentsTieringSchema.resource": False,
    "NasApplicationComponentsTieringSchema.opts": False,
    "NasApplicationComponentsTiering": False,
}


class NasApplicationComponentsTieringSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the NasApplicationComponentsTiering object"""

    control = fields.Str(data_key="control")
    r""" Storage tiering placement rules for the container(s)

Valid choices:

* required
* best_effort
* disallowed """

    object_stores = fields.List(fields.Nested("netapp_ontap.models.nas_application_components_tiering_object_stores.NasApplicationComponentsTieringObjectStoresSchema", unknown=EXCLUDE), data_key="object_stores")
    r""" The object_stores field of the nas_application_components_tiering. """

    policy = fields.Str(data_key="policy")
    r""" The storage tiering type of the application component.

Valid choices:

* all
* auto
* none
* snapshot_only """

    @property
    def resource(self):
        return NasApplicationComponentsTiering

    gettable_fields = [
        "policy",
    ]
    """policy,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
        "control",
        "object_stores",
        "policy",
    ]
    """control,object_stores,policy,"""


class NasApplicationComponentsTiering(Resource):

    _schema = NasApplicationComponentsTieringSchema
