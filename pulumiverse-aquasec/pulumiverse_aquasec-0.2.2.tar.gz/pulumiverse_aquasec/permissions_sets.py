# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['PermissionsSetsArgs', 'PermissionsSets']

@pulumi.input_type
class PermissionsSetsArgs:
    def __init__(__self__, *,
                 actions: pulumi.Input[Sequence[pulumi.Input[str]]],
                 ui_access: pulumi.Input[bool],
                 author: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_super: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a PermissionsSets resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        :param pulumi.Input[bool] ui_access: Whether to allow UI access for users with this Permission Set.
        :param pulumi.Input[str] author: The name of the user who created the Permission Set.
        :param pulumi.Input[str] description: Free text description for the Permission Set.
        :param pulumi.Input[bool] is_super: Give the Permission Set full access, meaning all actions are allowed without restriction.
        :param pulumi.Input[str] name: The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        """
        pulumi.set(__self__, "actions", actions)
        pulumi.set(__self__, "ui_access", ui_access)
        if author is not None:
            pulumi.set(__self__, "author", author)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_super is not None:
            pulumi.set(__self__, "is_super", is_super)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter(name="uiAccess")
    def ui_access(self) -> pulumi.Input[bool]:
        """
        Whether to allow UI access for users with this Permission Set.
        """
        return pulumi.get(self, "ui_access")

    @ui_access.setter
    def ui_access(self, value: pulumi.Input[bool]):
        pulumi.set(self, "ui_access", value)

    @property
    @pulumi.getter
    def author(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user who created the Permission Set.
        """
        return pulumi.get(self, "author")

    @author.setter
    def author(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Free text description for the Permission Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isSuper")
    def is_super(self) -> Optional[pulumi.Input[bool]]:
        """
        Give the Permission Set full access, meaning all actions are allowed without restriction.
        """
        return pulumi.get(self, "is_super")

    @is_super.setter
    def is_super(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_super", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _PermissionsSetsState:
    def __init__(__self__, *,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_super: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ui_access: Optional[pulumi.Input[bool]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PermissionsSets resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        :param pulumi.Input[str] author: The name of the user who created the Permission Set.
        :param pulumi.Input[str] description: Free text description for the Permission Set.
        :param pulumi.Input[bool] is_super: Give the Permission Set full access, meaning all actions are allowed without restriction.
        :param pulumi.Input[str] name: The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        :param pulumi.Input[bool] ui_access: Whether to allow UI access for users with this Permission Set.
        :param pulumi.Input[str] updated_at: The date of the last modification of the Role.
        """
        if actions is not None:
            pulumi.set(__self__, "actions", actions)
        if author is not None:
            pulumi.set(__self__, "author", author)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if is_super is not None:
            pulumi.set(__self__, "is_super", is_super)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if ui_access is not None:
            pulumi.set(__self__, "ui_access", ui_access)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter
    def actions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        """
        return pulumi.get(self, "actions")

    @actions.setter
    def actions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "actions", value)

    @property
    @pulumi.getter
    def author(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the user who created the Permission Set.
        """
        return pulumi.get(self, "author")

    @author.setter
    def author(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "author", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Free text description for the Permission Set.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="isSuper")
    def is_super(self) -> Optional[pulumi.Input[bool]]:
        """
        Give the Permission Set full access, meaning all actions are allowed without restriction.
        """
        return pulumi.get(self, "is_super")

    @is_super.setter
    def is_super(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_super", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="uiAccess")
    def ui_access(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to allow UI access for users with this Permission Set.
        """
        return pulumi.get(self, "ui_access")

    @ui_access.setter
    def ui_access(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ui_access", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        The date of the last modification of the Role.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)


class PermissionsSets(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_super: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ui_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        The `PermissionsSets` resource manages your Permission Set within Aqua.

        ## Example Usage

        ```python
        import pulumi
        import pulumiverse_aquasec as aquasec

        my_terraform_perm_set = aquasec.PermissionsSets("myTerraformPermSet",
            actions=[
                "acl_policies.read",
                "acl_policies.write",
                "image_profiles.read",
                "image_profiles.write",
                "network_policies.read",
                "network_policies.write",
                "runtime_policies.read",
                "runtime_policies.write",
                "response_policies.read",
                "response_policies.write",
                "image_assurance.read",
                "image_assurance.write",
                "dashboard.read",
                "dashboard.write",
                "risk_explorer.read",
                "images.read",
                "images.write",
                "risks.host_images.read",
                "risks.host_images.write",
                "functions.read",
                "functions.write",
                "enforcers.read",
                "enforcers.write",
                "containers.read",
                "services.read",
                "services.write",
                "infrastructure.read",
                "infrastructure.write",
                "risks.vulnerabilities.read",
                "risks.vulnerabilities.write",
                "risks.benchmark.read",
                "risks.benchmark.write",
                "audits.read",
                "secrets.read",
                "secrets.write",
                "settings.read",
                "settings.write",
                "integrations.read",
                "integrations.write",
                "registries_integrations.read",
                "registries_integrations.write",
                "scan.read",
                "gateways.read",
                "gateways.write",
                "consoles.read",
                "web_hook.read",
                "incidents.read",
            ],
            author="system",
            description="Test Permissions Sets created by Terraform",
            is_super=False,
            ui_access=True)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        :param pulumi.Input[str] author: The name of the user who created the Permission Set.
        :param pulumi.Input[str] description: Free text description for the Permission Set.
        :param pulumi.Input[bool] is_super: Give the Permission Set full access, meaning all actions are allowed without restriction.
        :param pulumi.Input[str] name: The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        :param pulumi.Input[bool] ui_access: Whether to allow UI access for users with this Permission Set.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PermissionsSetsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `PermissionsSets` resource manages your Permission Set within Aqua.

        ## Example Usage

        ```python
        import pulumi
        import pulumiverse_aquasec as aquasec

        my_terraform_perm_set = aquasec.PermissionsSets("myTerraformPermSet",
            actions=[
                "acl_policies.read",
                "acl_policies.write",
                "image_profiles.read",
                "image_profiles.write",
                "network_policies.read",
                "network_policies.write",
                "runtime_policies.read",
                "runtime_policies.write",
                "response_policies.read",
                "response_policies.write",
                "image_assurance.read",
                "image_assurance.write",
                "dashboard.read",
                "dashboard.write",
                "risk_explorer.read",
                "images.read",
                "images.write",
                "risks.host_images.read",
                "risks.host_images.write",
                "functions.read",
                "functions.write",
                "enforcers.read",
                "enforcers.write",
                "containers.read",
                "services.read",
                "services.write",
                "infrastructure.read",
                "infrastructure.write",
                "risks.vulnerabilities.read",
                "risks.vulnerabilities.write",
                "risks.benchmark.read",
                "risks.benchmark.write",
                "audits.read",
                "secrets.read",
                "secrets.write",
                "settings.read",
                "settings.write",
                "integrations.read",
                "integrations.write",
                "registries_integrations.read",
                "registries_integrations.write",
                "scan.read",
                "gateways.read",
                "gateways.write",
                "consoles.read",
                "web_hook.read",
                "incidents.read",
            ],
            author="system",
            description="Test Permissions Sets created by Terraform",
            is_super=False,
            ui_access=True)
        ```

        :param str resource_name: The name of the resource.
        :param PermissionsSetsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PermissionsSetsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 is_super: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ui_access: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PermissionsSetsArgs.__new__(PermissionsSetsArgs)

            if actions is None and not opts.urn:
                raise TypeError("Missing required property 'actions'")
            __props__.__dict__["actions"] = actions
            __props__.__dict__["author"] = author
            __props__.__dict__["description"] = description
            __props__.__dict__["is_super"] = is_super
            __props__.__dict__["name"] = name
            if ui_access is None and not opts.urn:
                raise TypeError("Missing required property 'ui_access'")
            __props__.__dict__["ui_access"] = ui_access
            __props__.__dict__["updated_at"] = None
        super(PermissionsSets, __self__).__init__(
            'aquasec:index/permissionsSets:PermissionsSets',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            actions: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            author: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            is_super: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            ui_access: Optional[pulumi.Input[bool]] = None,
            updated_at: Optional[pulumi.Input[str]] = None) -> 'PermissionsSets':
        """
        Get an existing PermissionsSets resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] actions: List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        :param pulumi.Input[str] author: The name of the user who created the Permission Set.
        :param pulumi.Input[str] description: Free text description for the Permission Set.
        :param pulumi.Input[bool] is_super: Give the Permission Set full access, meaning all actions are allowed without restriction.
        :param pulumi.Input[str] name: The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        :param pulumi.Input[bool] ui_access: Whether to allow UI access for users with this Permission Set.
        :param pulumi.Input[str] updated_at: The date of the last modification of the Role.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PermissionsSetsState.__new__(_PermissionsSetsState)

        __props__.__dict__["actions"] = actions
        __props__.__dict__["author"] = author
        __props__.__dict__["description"] = description
        __props__.__dict__["is_super"] = is_super
        __props__.__dict__["name"] = name
        __props__.__dict__["ui_access"] = ui_access
        __props__.__dict__["updated_at"] = updated_at
        return PermissionsSets(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def actions(self) -> pulumi.Output[Sequence[str]]:
        """
        List of allowed actions for the Permission Set (not relevant if 'is_super' is true).
        """
        return pulumi.get(self, "actions")

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the user who created the Permission Set.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Free text description for the Permission Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="isSuper")
    def is_super(self) -> pulumi.Output[Optional[bool]]:
        """
        Give the Permission Set full access, meaning all actions are allowed without restriction.
        """
        return pulumi.get(self, "is_super")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the Permission Set, comprised of alphanumeric characters and '-', '_', ' ', ':', '.', '@', '!', '^'.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="uiAccess")
    def ui_access(self) -> pulumi.Output[bool]:
        """
        Whether to allow UI access for users with this Permission Set.
        """
        return pulumi.get(self, "ui_access")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The date of the last modification of the Role.
        """
        return pulumi.get(self, "updated_at")

