# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.repository.v1 import plugin_pb2 as spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2


class PluginStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.register = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/register',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.CreatePluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/update',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.UpdatePluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
                )
        self.deregister = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/deregister',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/enable',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/disable',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
                )
        self.get_versions = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/get_versions',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.RepositoryPluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.VersionsInfo.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/get',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.GetRepositoryPluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/list',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.repository.v1.Plugin/stat',
                request_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class PluginServicer(object):
    """Missing associated documentation comment in .proto file."""

    def register(self, request, context):
        """
        desc: Registers a Plugin. The parameter `registry_type`, meaning container registry type, can be either `DOCKER_HUB` or `AWS_PUBLIC_ECR`. The default value of the `registry_type` is `DOCKER_HUB`. The parameter `registry_url` is required if the `registry_type` is not `DOCKER_HUB`. The parameter `image` is limited to 40 characters.
        request_example: >-
        {
        "name": "JIRA Issue notification",
        "service_type": "notification.Procotol",
        "image": "pyengine/plugin-jira-noti-protocol",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "provider": "atlassian",
        "capability": {
        "supported_schema": [
        "atlassian_jira"
        ]
        },
        "template": {
        "options": {
        "schema": {
        "type": "object",
        "required": [],
        "properties": {
        "project_id": {
        "type": "string",
        "title": "Project ID",
        "minLength": 4.0
        },
        "sa_name": {
        "title": "Service Account",
        "type": "string",
        "minLength": 4.0
        }
        }
        }
        }
        },
        "labels": [
        "jira",
        "atlassian",
        "notification"
        ],
        "tags": {
        "description": "Atlassian JIRA Issue notification",
        "icon": "https://icon-path/jira-icon.png"
        }
        }
        response_example: >-
        {
        "plugin_id": "plugin-jira-noti-protocol",
        "name": "JIRA Issue notification",
        "image": "pyengine/plugin-jira-noti-protocol",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "notification.Procotol",
        "provider": "atlassian",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {
        "supported_schema": [
        "atlassian_jira"
        ]
        },
        "template": {
        "options": {
        "schema": {
        "type": "object",
        "required": [],
        "properties": {
        "project_id": {
        "type": "string",
        "title": "Project ID",
        "minLength": 4.0
        },
        "sa_name": {
        "title": "Service Account",
        "type": "string",
        "minLength": 4.0
        }
        }
        }
        }
        },
        "labels": [
        "jira",
        "atlassian",
        "notification"
        ],
        "tags": {
        "description": "Atlassian JIRA Issue notification",
        "icon": "https://icon-path/jira-icon.png"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-123456789012",
        "created_at": "2022-01-01T08:02:38.094Z",
        "updated_at": "2022-01-01T08:02:38.094Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        desc: Updates a specific Plugin registered. A Plugin can be updated only if its Repository's `repository_type` is `local`. You can make changes in Plugin settings, including `template` and its options, `schema`.
        request_example: >-
        {
        "name": "JIRA Issue notification",
        "capability": {
        "supported_schema": [
        "atlassian_jira"
        ]
        },
        "template": {
        "options": {
        "schema": {
        "type": "object",
        "required": [],
        "properties": {
        "project_id": {
        "type": "string",
        "title": "Project ID",
        "minLength": 4.0
        },
        "sa_name": {
        "title": "Service Account",
        "type": "string",
        "minLength": 4.0
        }
        }
        }
        }
        },
        "labels": [
        "jira",
        "atlassian",
        "notification"
        ],
        "tags": {
        "description": "Atlassian JIRA Issue notification",
        "icon": "https://icon-path/jira-icon.png"
        }
        }
        response_example: >-
        {
        "plugin_id": "plugin-jira-noti-protocol",
        "name": "JIRA Issue notification",
        "image": "pyengine/plugin-jira-noti-protocol",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "notification.Procotol",
        "provider": "atlassian",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {
        "supported_schema": [
        "atlassian_jira"
        ]
        },
        "template": {
        "options": {
        "schema": {
        "type": "object",
        "required": [],
        "properties": {
        "project_id": {
        "type": "string",
        "title": "Project ID",
        "minLength": 4.0
        },
        "sa_name": {
        "title": "Service Account",
        "type": "string",
        "minLength": 4.0
        }
        }
        }
        }
        },
        "labels": [
        "jira",
        "atlassian",
        "notification"
        ],
        "tags": {
        "description": "Atlassian JIRA Issue notification",
        "spaceone:plugin_name": "plugin-jira-noti-protocol",
        "icon": "https://icon-path/jira-icon.png"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-123456789012",
        "created_at": "2022-01-01T08:02:38.094Z",
        "updated_at": "2022-01-01T08:02:38.094Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deregister(self, request, context):
        """
        desc: Deregisters and deletes a specific Plugin. You must specify the `plugin_id` of the Plugin to deregister.
        request_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "domain_id": "domain-123456789012"
        }
        response_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "name": "AWS SNS Webhook",
        "image": "pyengine/plugin-aws-sns-mon-webhook",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "monitoring.Webhook",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {
        "icon": "https://icon-path/Amazon-SNS.svg"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2022-01-01T08:14:23.175Z",
        "updated_at": "2022-01-01T08:14:23.175Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """
        desc: Enables a specific Plugin. If the Plugin is enabled, the Plugin can be used as its parameter `state` becomes `ENABLED`.
        request_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "domain_id": "domain-123456789012"
        }
        response_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "name": "AWS SNS Webhook",
        "image": "pyengine/plugin-aws-sns-mon-webhook",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "monitoring.Webhook",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {
        "icon": "https://icon-path/Amazon-SNS.svg"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2022-01-01T08:14:23.175Z",
        "updated_at": "2022-01-01T08:14:23.175Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """
        desc: Disables a specific Plugin. If the Plugin is disabled, the Plugin cannot be used as its parameter `state` becomes `DISABLED`.
        request_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "domain_id": "domain-123456789012"
        }
        response_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "name": "AWS SNS Webhook",
        "image": "pyengine/plugin-aws-sns-mon-webhook",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "monitoring.Webhook",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {
        "icon": "https://icon-path/Amazon-SNS.svg"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2022-01-01T08:14:23.175Z",
        "updated_at": "2022-01-01T08:14:23.175Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_versions(self, request, context):
        """
        desc: Gets all version data of a specific Plugin from its Repository. The parameter `plugin_id` is used as an identifier of a Plugin to get version data.
        request_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "domain_id": "domain-123456789012"
        }
        response_example: >-
        {
        "total_count": 1,
        "results": [
        "1.2.2",
        "1.2.1.20220429.104002",
        "1.2.1.20220422.161421",
        "1.2.1.20220411.113807",
        "1.2.1"
        ]
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        desc: Gets a specific Plugin. Prints detailed information about the Plugin, including  `image`, `registry_url`, and `state`.
        request_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "domain_id": "domain-123456789012"
        }
        response_example: >-
        {
        "plugin_id": "plugin-aws-sns-mon-webhook",
        "name": "AWS SNS Webhook",
        "image": "pyengine/plugin-aws-sns-mon-webhook",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "monitoring.Webhook",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {
        "icon": "https://icon-url/Amazon-SNS.svg"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2021-06-14T08:14:23.175Z",
        "updated_at": "2021-06-14T08:14:23.175Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        desc: Gets a list of all Plugins registered in a specific Repository. The parameter `repository_id` is used as an identifier of a Repository to get its list of Plugins. You can use a query to get a filtered list of Plugins.
        request_example: >-
        {
        "query": {},
        "repository_id": "repo-123456789012"
        }
        response_example: >-
        {
        "results": [
        {
        "plugin_id": "plugin-api-direct-mon-webhook",
        "name": "API Direct Webhook",
        "image": "pyengine/plugin-api-direct-mon-webhook",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "monitoring.Webhook",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {
        "icon": "https://icon-url/icon.svg"
        },
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2022-01-01T03:25:10.408Z",
        "updated_at": "2022-01-01T03:25:10.408Z"
        },
        {
        "plugin_id": "plugin-aws-hyperbilling-cost-datasource",
        "name": "AWS HyperBilling Cost Analysis Data Source",
        "image": "pyengine/plugin-aws-hyperbilling-cost-datasource",
        "registry_url": "registry.hub.docker.com",
        "state": "ENABLED",
        "service_type": "cost_analysis.DataSoruce",
        "registry_type": "DOCKER_HUB",
        "registry_config": {},
        "capability": {},
        "template": {},
        "labels": [],
        "tags": {},
        "repository_info": {
        "repository_id": "repo-123456789012",
        "name": "Marketplace",
        "repository_type": "remote"
        },
        "domain_id": "domain-987654321098",
        "created_at": "2022-01-01T04:56:55.082Z",
        "updated_at": "2022-01-01T04:56:55.082Z"
        }
        ],
        "total_count": 2
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PluginServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.CreatePluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.UpdatePluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.SerializeToString,
            ),
            'deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.deregister,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.SerializeToString,
            ),
            'get_versions': grpc.unary_unary_rpc_method_handler(
                    servicer.get_versions,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.RepositoryPluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.VersionsInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.GetRepositoryPluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.repository.v1.Plugin', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Plugin(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def register(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/register',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.CreatePluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/update',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.UpdatePluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def deregister(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/deregister',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/enable',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/disable',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_versions(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/get_versions',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.RepositoryPluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.VersionsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/get',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.GetRepositoryPluginRequest.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/list',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginQuery.SerializeToString,
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.repository.v1.Plugin/stat',
            spaceone_dot_api_dot_repository_dot_v1_dot_plugin__pb2.PluginStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
