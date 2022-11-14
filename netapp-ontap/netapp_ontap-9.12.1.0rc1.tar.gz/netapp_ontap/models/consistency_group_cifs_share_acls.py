r"""
Copyright &copy; 2022 NetApp Inc.
All rights reserved.

This file has been automatically generated based on the ONTAP REST API documentation.

"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema, ResourceSchemaMeta, ImpreciseDateTime, Size


__all__ = ["ConsistencyGroupCifsShareAcls", "ConsistencyGroupCifsShareAclsSchema"]
__pdoc__ = {
    "ConsistencyGroupCifsShareAclsSchema.resource": False,
    "ConsistencyGroupCifsShareAclsSchema.opts": False,
    "ConsistencyGroupCifsShareAcls": False,
}


class ConsistencyGroupCifsShareAclsSchema(ResourceSchema, metaclass=ResourceSchemaMeta):
    """The fields of the ConsistencyGroupCifsShareAcls object"""

    links = fields.Nested("netapp_ontap.models.self_link.SelfLinkSchema", unknown=EXCLUDE, data_key="_links")
    r""" The links field of the consistency_group_cifs_share_acls. """

    permission = fields.Str(data_key="permission")
    r""" Specifies the access rights that a user or group has on the defined CIFS Share.
The following values are allowed:

* no_access    - User does not have CIFS share access
* read         - User has only read access
* change       - User has change access
* full_control - User has full_control access


Valid choices:

* no_access
* read
* change
* full_control """

    type = fields.Str(data_key="type")
    r""" Specifies the type of the user or group to add to the access control
list of a CIFS share. The following values are allowed:

* windows    - Windows user or group
* unix_user  - UNIX user
* unix_group - UNIX group


Valid choices:

* windows
* unix_user
* unix_group """

    user_or_group = fields.Str(data_key="user_or_group")
    r""" Specifies the user or group name to add to the access control list of a CIFS share.

Example: ENGDOMAIN\ad_user """

    @property
    def resource(self):
        return ConsistencyGroupCifsShareAcls

    gettable_fields = [
        "links",
        "permission",
        "type",
        "user_or_group",
    ]
    """links,permission,type,user_or_group,"""

    patchable_fields = [
        "permission",
    ]
    """permission,"""

    postable_fields = [
        "permission",
        "type",
        "user_or_group",
    ]
    """permission,type,user_or_group,"""


class ConsistencyGroupCifsShareAcls(Resource):

    _schema = ConsistencyGroupCifsShareAclsSchema
