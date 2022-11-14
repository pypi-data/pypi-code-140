from abc import ABC, abstractmethod
from types import SimpleNamespace

from cli_ui import fatal, warning
from ruamel.yaml.comments import CommentedMap
from yamlpath import Processor
from yamlpath.exceptions import YAMLPathException
from yamlpath.wrappers import ConsolePrinter

from gitlabform.constants import EXIT_INVALID_INPUT, APPROVAL_RULE_NAME
from gitlabform.configuration import Configuration
from gitlabform.gitlab import AccessLevel
from gitlabform.gitlab import GitLab


# Configuration transformers are classes which take the input configuration as YAML and change it
# to from the more user-friendly input to an output that is more applicable to passing to GitLab
# over its API.
#
# For example, we want to operate on usernames in the configuration while GitLab sometimes operates
# on user ids. Therefore, one of the transformers changes "user_id: <number>" into "user: <username>".


class ConfigurationTransformers:
    def __init__(self, gitlab: GitLab):
        self.merge_request_approvals_transformer = MergeRequestApprovalsTransformer(
            gitlab
        )
        self.user_transformer = UserTransformer(gitlab)
        self.group_transformer = GroupTransformer(gitlab)
        self.implicit_name_transformer = ImplicitNameTransformer(gitlab)
        self.access_level_transformer = AccessLevelsTransformer(gitlab)

    def transform(self, configuration: Configuration) -> None:
        # this needs to run before user and group transformer as it may contain users and group
        # names to convert to ids
        self.merge_request_approvals_transformer.transform(configuration)

        self.user_transformer.transform(configuration)
        self.group_transformer.transform(configuration)
        self.implicit_name_transformer.transform(configuration)
        self.access_level_transformer.transform(configuration)


class ConfigurationTransformer(ABC):
    @abstractmethod
    def transform(self, configuration: Configuration) -> None:
        pass


class UserTransformer(ConfigurationTransformer):
    def __init__(self, gitlab: GitLab):
        self.gitlab = gitlab

    def transform(self, configuration: Configuration) -> None:
        logging_args = SimpleNamespace(quiet=False, verbose=False, debug=False)

        processor = Processor(ConsolePrinter(logging_args), configuration.config)

        paths_to_user = [
            "projects_and_groups.*.protected_environments.*.deploy_access_levels.user"
        ]

        for path in paths_to_user:
            try:
                for node_coordinate in processor.get_nodes(path):
                    user = node_coordinate.parent.pop("user")

                    node_coordinate.parent["user_id"] = self.gitlab._get_user_id(user)
            except YAMLPathException as e:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass

        paths_to_users = ["projects_and_groups.*.merge_requests_approval_rules.*.users"]

        for path in paths_to_users:
            try:
                for node_coordinate in processor.get_nodes(path):
                    user_ids = []
                    users = node_coordinate.parent.pop("users")
                    for user in users:
                        user_id = self.gitlab._get_user_id(user)
                        user_ids.append(user_id)
                    node_coordinate.parent["user_ids"] = user_ids
            except YAMLPathException as e:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass


class GroupTransformer(ConfigurationTransformer):
    def __init__(self, gitlab: GitLab):
        self.gitlab = gitlab

    def transform(self, configuration: Configuration) -> None:
        logging_args = SimpleNamespace(quiet=False, verbose=False, debug=False)

        processor = Processor(ConsolePrinter(logging_args), configuration.config)

        paths_to_groups = [
            "projects_and_groups.*.merge_requests_approval_rules.*.groups"
        ]

        for path in paths_to_groups:
            try:
                for node_coordinate in processor.get_nodes(path):
                    group_ids = []
                    groups = node_coordinate.parent.pop("groups")
                    for group in groups:
                        group_id = self.gitlab._get_group_id(group)
                        group_ids.append(group_id)
                    node_coordinate.parent["group_ids"] = group_ids
            except YAMLPathException:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass


class ImplicitNameTransformer(ConfigurationTransformer):
    """
    Creates a 'name' field that has the same value as the "scope" delimiter, e.g.:

    ...
      blah: # start of the cfg scope
       name: blah # name to be used
       smth_else: <...>

    It's redundant, so this can be done as :

    ...
     foo: # a 'name' field will be created as -> name: foo
       smth_else: <...>
    """

    def __init__(self, gitlab: GitLab):
        # this transformer doesn't need to call gitlab
        pass

    def transform(self, configuration: Configuration) -> None:
        logging_args = SimpleNamespace(quiet=False, verbose=False, debug=False)

        processor = Processor(ConsolePrinter(logging_args), configuration.config)

        paths_to_implicit_names = ["projects_and_groups.*.protected_environments.*"]

        for path in paths_to_implicit_names:
            try:
                for node_coordinate in processor.get_nodes(path):
                    if not isinstance(node_coordinate.node, CommentedMap):
                        continue

                    node_coordinate.parent[node_coordinate.parentref][
                        "name"
                    ] = node_coordinate.parentref
            except YAMLPathException:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass


class AccessLevelsTransformer(ConfigurationTransformer):
    """
    Internally the app supports only numeric access levels, but for user-friendliness
    this class allows providing them as strings and transforms these strings into
    the appropriate numbers.
    """

    def __init__(self, gitlab: GitLab):
        # this transformer doesn't need to call gitlab
        pass

    def transform(self, configuration: Configuration):
        logging_args = SimpleNamespace(quiet=False, verbose=False, debug=False)
        log = ConsolePrinter(logging_args)

        processor = Processor(log, configuration.config)

        # [.!<100] effectively means that the value is non-numerical
        paths_to_hashes = [
            # # branches, old syntax
            "**.push_access_level[.!<100]",
            "**.merge_access_level[.!<100]",
            "**.unprotect_access_level[.!<100]",
            # members & group members
            "**.access_level[.!<100]",
            "**.group_access[.!<100]",
            # old syntax
            "**.group_access_level[.!<100]",
            # tags
            "**.create_access_level[.!<100]",
        ]

        for path in paths_to_hashes:
            try:
                for node_coordinate in processor.get_nodes(path):
                    try:
                        access_level_string = str(node_coordinate.node)
                        node_coordinate.parent[
                            node_coordinate.parentref
                        ] = AccessLevel.get_value(access_level_string)
                    except KeyError:
                        fatal(
                            f"Configuration string '{access_level_string}' is not one of the valid access levels:"
                            f" {', '.join(AccessLevel.get_canonical_names())}",
                            exit_code=EXIT_INVALID_INPUT,
                        )
            except YAMLPathException:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass

        # these are different from the above, as they are elements of arrays,
        # so we need different search query and an extra condition for
        # transformation
        paths_to_arrays = [
            # # branches, new GitLab Premium syntax
            "**.allowed_to_push.*.[access_level!<100]",
            "**.allowed_to_merge.*.[access_level!<100]",
            "**.allowed_to_unprotect.*.[access_level!<100]",
        ]

        for path in paths_to_arrays:
            try:
                for node_coordinate in processor.get_nodes(path):
                    if node_coordinate.parentref == "access_level":
                        try:
                            access_level_string = str(node_coordinate.node)
                            node_coordinate.parent[
                                node_coordinate.parentref
                            ] = AccessLevel.get_value(access_level_string)
                        except KeyError:
                            fatal(
                                f"Configuration string '{access_level_string}' is not one of the valid access levels:"
                                f" {', '.join(AccessLevel.get_canonical_names())}",
                                exit_code=EXIT_INVALID_INPUT,
                            )
            except YAMLPathException:
                # this just means that we haven't found any keys in YAML
                # under the given path
                pass


#
# TODO: remove below code in v4.x
#


class MergeRequestApprovalsTransformer(ConfigurationTransformer):
    def __init__(self, gitlab: GitLab):
        # this transformer doesn't need to call gitlab
        pass

    def transform(self, configuration: Configuration) -> None:
        logging_args = SimpleNamespace(quiet=False, verbose=False, debug=False)

        processor = Processor(ConsolePrinter(logging_args), configuration.config)

        try:
            for node_coordinate in processor.get_nodes(
                "projects_and_groups.*.merge_requests"
            ):
                old_syntax_found = False

                where_to_add_new_syntax = node_coordinate.parent

                old_syntax = node_coordinate.node

                # approval rules
                if "approvers" in old_syntax or "approver_groups" in old_syntax:
                    old_syntax_found = True

                    # we shouldn't have accepted this syntax before, but we did and now it's a problem
                    # because what should be the default approvals required setting? :/
                    if (
                        "approvals" in old_syntax
                        and "approvals_before_merge" in old_syntax["approvals"]
                    ):
                        approvals_required = old_syntax["approvals"][
                            "approvals_before_merge"
                        ]
                    else:
                        approvals_required = 2

                    where_to_add_new_syntax["merge_requests_approval_rules"] = {
                        "legacy": {
                            "approvals_required": approvals_required,
                            "name": APPROVAL_RULE_NAME,
                        }
                    }

                    if "approvers" in old_syntax:
                        where_to_add_new_syntax["merge_requests_approval_rules"][
                            "legacy"
                        ]["users"] = old_syntax["approvers"]
                    if "approver_groups" in old_syntax:
                        where_to_add_new_syntax["merge_requests_approval_rules"][
                            "legacy"
                        ]["groups"] = old_syntax["approver_groups"]

                    if (
                        "remove_other_approval_rules" in old_syntax
                        and old_syntax["remove_other_approval_rules"]
                    ):
                        old_syntax_found = True
                        where_to_add_new_syntax["merge_requests_approval_rules"][
                            "enforce"
                        ] = True

                # approvals configurations
                if "approvals" in old_syntax:
                    old_syntax_found = True
                    if "approvals_before_merge" in old_syntax["approvals"]:
                        # this setting is now moved inside the approval rules, so remove it from here
                        old_syntax["approvals"].pop("approvals_before_merge")
                    where_to_add_new_syntax["merge_requests_approvals"] = old_syntax[
                        "approvals"
                    ]

                if old_syntax_found:
                    warning(
                        "The 'merge_requests' configuration section syntax works but is deprecated and will be removed "
                        "in the next major version of GitLabForm. "
                        "Please migrate to the new syntax using the 'merge_requests_approvals' "
                        "and the 'merge_requests_approval_rules' sections."
                    )

        except YAMLPathException:
            # this just means that we haven't found any keys in YAML
            # under the given path
            pass
