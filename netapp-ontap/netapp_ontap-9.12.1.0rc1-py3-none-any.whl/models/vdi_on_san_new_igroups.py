r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["VdiOnSanNewIgroups", "VdiOnSanNewIgroupsSchema"]
__pdoc__ = {
    "VdiOnSanNewIgroupsSchema.resource": False,
    "VdiOnSanNewIgroupsSchema.opts": False,
    "VdiOnSanNewIgroups": False,
}


class VdiOnSanNewIgroupsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the VdiOnSanNewIgroups object"""

    comment = fields.Str(data_key="comment")
    r""" A comment available for use by the administrator. """

    igroups = fields.List(fields.Nested("netapp_ontap.models.mongo_db_on_san_new_igroups_igroups.MongoDbOnSanNewIgroupsIgroupsSchema", unknown=EXCLUDE), data_key="igroups")
    r""" The igroups field of the vdi_on_san_new_igroups. """

    initiator_objects = fields.List(fields.Nested("netapp_ontap.models.mongo_db_on_san_new_igroups_initiator_objects.MongoDbOnSanNewIgroupsInitiatorObjectsSchema", unknown=EXCLUDE), data_key="initiator_objects")
    r""" The initiator_objects field of the vdi_on_san_new_igroups. """

    initiators = fields.List(fields.Str, data_key="initiators")
    r""" The initiators field of the vdi_on_san_new_igroups. """

    name = fields.Str(data_key="name")
    r""" The name of the new initiator group. """

    protocol = fields.Str(data_key="protocol")
    r""" The protocol of the new initiator group.

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return VdiOnSanNewIgroups

    gettable_fields = [
        "initiators",
    ]
    """initiators,"""

    patchable_fields = [
        "comment",
        "igroups",
        "initiator_objects",
        "initiators",
        "name",
        "protocol",
    ]
    """comment,igroups,initiator_objects,initiators,name,protocol,"""

    postable_fields = [
        "comment",
        "igroups",
        "initiator_objects",
        "initiators",
        "name",
        "protocol",
    ]
    """comment,igroups,initiator_objects,initiators,name,protocol,"""


class VdiOnSanNewIgroups(Resource):

    _schema = VdiOnSanNewIgroupsSchema
