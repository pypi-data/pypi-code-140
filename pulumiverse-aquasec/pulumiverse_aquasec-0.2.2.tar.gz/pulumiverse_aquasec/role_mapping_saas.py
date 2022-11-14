# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['RoleMappingSaasArgs', 'RoleMappingSaas']

@pulumi.input_type
class RoleMappingSaasArgs:
    def __init__(__self__, *,
                 csp_role: pulumi.Input[str],
                 saml_groups: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        The set of arguments for constructing a RoleMappingSaas resource.
        """
        pulumi.set(__self__, "csp_role", csp_role)
        pulumi.set(__self__, "saml_groups", saml_groups)

    @property
    @pulumi.getter(name="cspRole")
    def csp_role(self) -> pulumi.Input[str]:
        return pulumi.get(self, "csp_role")

    @csp_role.setter
    def csp_role(self, value: pulumi.Input[str]):
        pulumi.set(self, "csp_role", value)

    @property
    @pulumi.getter(name="samlGroups")
    def saml_groups(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "saml_groups")

    @saml_groups.setter
    def saml_groups(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "saml_groups", value)


@pulumi.input_type
class _RoleMappingSaasState:
    def __init__(__self__, *,
                 account_id: Optional[pulumi.Input[int]] = None,
                 created: Optional[pulumi.Input[str]] = None,
                 csp_role: Optional[pulumi.Input[str]] = None,
                 role_mapping_id: Optional[pulumi.Input[int]] = None,
                 saml_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering RoleMappingSaas resources.
        """
        if account_id is not None:
            pulumi.set(__self__, "account_id", account_id)
        if created is not None:
            pulumi.set(__self__, "created", created)
        if csp_role is not None:
            pulumi.set(__self__, "csp_role", csp_role)
        if role_mapping_id is not None:
            pulumi.set(__self__, "role_mapping_id", role_mapping_id)
        if saml_groups is not None:
            pulumi.set(__self__, "saml_groups", saml_groups)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "account_id")

    @account_id.setter
    def account_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "account_id", value)

    @property
    @pulumi.getter
    def created(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "created")

    @created.setter
    def created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created", value)

    @property
    @pulumi.getter(name="cspRole")
    def csp_role(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "csp_role")

    @csp_role.setter
    def csp_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "csp_role", value)

    @property
    @pulumi.getter(name="roleMappingId")
    def role_mapping_id(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "role_mapping_id")

    @role_mapping_id.setter
    def role_mapping_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "role_mapping_id", value)

    @property
    @pulumi.getter(name="samlGroups")
    def saml_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "saml_groups")

    @saml_groups.setter
    def saml_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "saml_groups", value)


class RoleMappingSaas(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 csp_role: Optional[pulumi.Input[str]] = None,
                 saml_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumiverse_aquasec as aquasec

        roles_mapping_saas_role_mapping_saas = aquasec.RoleMappingSaas("rolesMappingSaasRoleMappingSaas",
            saml_groups=[
                "group1",
                "group2",
            ],
            csp_role="Administrator")
        pulumi.export("rolesMappingSaas", roles_mapping_saas_role_mapping_saas)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RoleMappingSaasArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumiverse_aquasec as aquasec

        roles_mapping_saas_role_mapping_saas = aquasec.RoleMappingSaas("rolesMappingSaasRoleMappingSaas",
            saml_groups=[
                "group1",
                "group2",
            ],
            csp_role="Administrator")
        pulumi.export("rolesMappingSaas", roles_mapping_saas_role_mapping_saas)
        ```

        :param str resource_name: The name of the resource.
        :param RoleMappingSaasArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RoleMappingSaasArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 csp_role: Optional[pulumi.Input[str]] = None,
                 saml_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RoleMappingSaasArgs.__new__(RoleMappingSaasArgs)

            if csp_role is None and not opts.urn:
                raise TypeError("Missing required property 'csp_role'")
            __props__.__dict__["csp_role"] = csp_role
            if saml_groups is None and not opts.urn:
                raise TypeError("Missing required property 'saml_groups'")
            __props__.__dict__["saml_groups"] = saml_groups
            __props__.__dict__["account_id"] = None
            __props__.__dict__["created"] = None
            __props__.__dict__["role_mapping_id"] = None
        super(RoleMappingSaas, __self__).__init__(
            'aquasec:index/roleMappingSaas:RoleMappingSaas',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            account_id: Optional[pulumi.Input[int]] = None,
            created: Optional[pulumi.Input[str]] = None,
            csp_role: Optional[pulumi.Input[str]] = None,
            role_mapping_id: Optional[pulumi.Input[int]] = None,
            saml_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'RoleMappingSaas':
        """
        Get an existing RoleMappingSaas resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RoleMappingSaasState.__new__(_RoleMappingSaasState)

        __props__.__dict__["account_id"] = account_id
        __props__.__dict__["created"] = created
        __props__.__dict__["csp_role"] = csp_role
        __props__.__dict__["role_mapping_id"] = role_mapping_id
        __props__.__dict__["saml_groups"] = saml_groups
        return RoleMappingSaas(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> pulumi.Output[int]:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        return pulumi.get(self, "created")

    @property
    @pulumi.getter(name="cspRole")
    def csp_role(self) -> pulumi.Output[str]:
        return pulumi.get(self, "csp_role")

    @property
    @pulumi.getter(name="roleMappingId")
    def role_mapping_id(self) -> pulumi.Output[int]:
        return pulumi.get(self, "role_mapping_id")

    @property
    @pulumi.getter(name="samlGroups")
    def saml_groups(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "saml_groups")

