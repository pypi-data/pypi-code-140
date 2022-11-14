from gitlabform.gitlab import GitLab
from gitlabform.processors.defining_keys import Key, And
from gitlabform.processors.multiple_entities_processor import MultipleEntitiesProcessor


class MergeRequestsApprovalRules(MultipleEntitiesProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__(
            "merge_requests_approval_rules",
            gitlab,
            list_method_name="get_approval_rules",
            add_method_name="add_approval_rule",
            edit_method_name="edit_approval_rule",
            delete_method_name="delete_approval_rule",
            defining=Key("name"),
            required_to_create_or_update=And(Key("name"), Key("approvals_required")),
        )
