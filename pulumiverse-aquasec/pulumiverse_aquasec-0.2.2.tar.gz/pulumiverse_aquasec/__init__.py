# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .application_scope import *
from .container_runtime_policy import *
from .enforcer_groups import *
from .firewall_policy import *
from .function_assurance_policy import *
from .function_runtime_policy import *
from .get_application_scope import *
from .get_container_runtime_policy import *
from .get_enforcer_groups import *
from .get_firewall_policy import *
from .get_function_assurance_policy import *
from .get_function_runtime_policy import *
from .get_gateways import *
from .get_groups import *
from .get_host_assurance_policy import *
from .get_host_runtime_policy import *
from .get_image import *
from .get_image_assurance_policy import *
from .get_integration_registry import *
from .get_integration_state import *
from .get_kubernetes_assurance_policy import *
from .get_permissions_sets import *
from .get_roles import *
from .get_roles_mapping import *
from .get_roles_mapping_saas import *
from .get_service import *
from .get_users import *
from .get_users_saas import *
from .group import *
from .host_assurance_policy import *
from .host_runtime_policy import *
from .image import *
from .image_assurance_policy import *
from .integration_registry import *
from .kubernetes_assurance_policy import *
from .notification_slack import *
from .permissions_sets import *
from .provider import *
from .role import *
from .role_mapping import *
from .role_mapping_saas import *
from .service import *
from .user import *
from .user_saas import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumiverse_aquasec.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumiverse_aquasec.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "aquasec",
  "mod": "index/applicationScope",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/applicationScope:ApplicationScope": "ApplicationScope"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/containerRuntimePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/containerRuntimePolicy:ContainerRuntimePolicy": "ContainerRuntimePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/enforcerGroups",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/enforcerGroups:EnforcerGroups": "EnforcerGroups"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/firewallPolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/firewallPolicy:FirewallPolicy": "FirewallPolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/functionAssurancePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/functionAssurancePolicy:FunctionAssurancePolicy": "FunctionAssurancePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/functionRuntimePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/functionRuntimePolicy:FunctionRuntimePolicy": "FunctionRuntimePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/group",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/group:Group": "Group"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/hostAssurancePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/hostAssurancePolicy:HostAssurancePolicy": "HostAssurancePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/hostRuntimePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/hostRuntimePolicy:HostRuntimePolicy": "HostRuntimePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/image",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/image:Image": "Image"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/imageAssurancePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/imageAssurancePolicy:ImageAssurancePolicy": "ImageAssurancePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/integrationRegistry",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/integrationRegistry:IntegrationRegistry": "IntegrationRegistry"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/kubernetesAssurancePolicy",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/kubernetesAssurancePolicy:KubernetesAssurancePolicy": "KubernetesAssurancePolicy"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/notificationSlack",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/notificationSlack:NotificationSlack": "NotificationSlack"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/permissionsSets",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/permissionsSets:PermissionsSets": "PermissionsSets"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/role",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/role:Role": "Role"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/roleMapping",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/roleMapping:RoleMapping": "RoleMapping"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/roleMappingSaas",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/roleMappingSaas:RoleMappingSaas": "RoleMappingSaas"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/service",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/service:Service": "Service"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/user",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/user:User": "User"
  }
 },
 {
  "pkg": "aquasec",
  "mod": "index/userSaas",
  "fqn": "pulumiverse_aquasec",
  "classes": {
   "aquasec:index/userSaas:UserSaas": "UserSaas"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "aquasec",
  "token": "pulumi:providers:aquasec",
  "fqn": "pulumiverse_aquasec",
  "class": "Provider"
 }
]
"""
)
