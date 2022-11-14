r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["EmsEventActionParametersTitleArguments", "EmsEventActionParametersTitleArgumentsSchema"]
__pdoc__ = {
    "EmsEventActionParametersTitleArgumentsSchema.resource": False,
    "EmsEventActionParametersTitleArgumentsSchema.opts": False,
    "EmsEventActionParametersTitleArguments": False,
}


class EmsEventActionParametersTitleArgumentsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the EmsEventActionParametersTitleArguments object"""

    code = fields.Str(data_key="code")
    r""" Argument code """

    message = fields.Str(data_key="message")
    r""" Message argument """

    @property
    def resource(self):
        return EmsEventActionParametersTitleArguments

    gettable_fields = [
        "code",
        "message",
    ]
    """code,message,"""

    patchable_fields = [
    ]
    """"""

    postable_fields = [
    ]
    """"""


class EmsEventActionParametersTitleArguments(Resource):

    _schema = EmsEventActionParametersTitleArgumentsSchema
