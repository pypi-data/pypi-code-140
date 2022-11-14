# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.plugin.v1 import supervisor_pb2 as spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2


class SupervisorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.publish = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/publish',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PublishSupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.register = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/register',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/update',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.deregister = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/deregister',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.enable = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/enable',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.disable = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/disable',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.recover_plugin = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/recover_plugin',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RecoverPluginRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginInfo.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/get',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.GetSupervisorRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/list',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/stat',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )
        self.list_plugins = channel.unary_unary(
                '/spaceone.api.plugin.v1.Supervisor/list_plugins',
                request_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginsInfo.FromString,
                )


class SupervisorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def publish(self, request, context):
        """
        desc: Creates a new Supervisor. Only Users with the `MANAGED` permission can set the Supervisor `public`. The Supervisor manages the lifecycle of plugin instances by the Supervisor's state. When a Supervisor is created, the state of the resource is `PENDING`. If the state remains the same for 5 minutes, the state is changed to `DISCONNECTED`.
        note: ''
        request_example: >-
        {
        "name": "test",
        "hostname": "dev-test2",
        "secret_key": "xxxxx",
        "tags": {
        "a": "b"
        }
        }
        response_example: >-
        {
        "supervisor_id": "supervisor-525982f2ae9a",
        "name": "test",
        "hostname": "dev-test2",
        "state": "ENABLED",
        "domain_id": "domain-1c5a6b8181ad",
        "tags": {
        "a": "b"
        },
        "labels": {},
        "created_at": "2022-01-15T05:42:02.999Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def register(self, request, context):
        """
        desc: Registers a specific Supervisor. You must specify the `supervisor_id` of the Supervisor to register. The `state` of the Supervisor changes from `PENDING` to `ENABLED`.
        note: ''
        request_example: >-
        {

        }
        response_example: >-
        {

        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        desc: Updates a specific Supervisor. You can make changes in Supervisor settings, including `labels`, `tags`, and the `bool` type parameter `is_public`.
        note: ''
        request_example: >-
        {
        "supervisor_id": "supervisor-525982f2ae9a",
        "is_public": true,
        "priority": 10,
        "labels": {
        "a": "b"
        },
        "tags": {
        "c": "d"
        },
        "domain_id": "domain-1c5a6b8181ad"
        }
        response_example: >-
        {
        "supervisor_id": "supervisor-525982f2ae9a",
        "name": "test",
        "hostname": "dev-test2",
        "state": "ENABLED",
        "is_public": true,
        "domain_id": "domain-1c5a6b8181ad",
        "tags": {
        "a": "b"
        },
        "labels": {
        "c": "d"
        },
        "created_at": "2022-06-15T05:42:02.999Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def deregister(self, request, context):
        """
        desc: Deregisters and deletes a specific Supervisor. You must specify the `supervisor_id` of the Supervisor to deregister.
        note: ''
        request_example: >-
        {
        "supervisor_id": "supervisor-d73011256d55"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """
        desc: Enables a specific Supervisor. By changing the `state` parameter to `ENABLED`, the Supervisor can deploy or delete the `pod` of the plugin instance.
        note: ''
        request_example: >-
        {
        "supervisor_id": "supervisor-d73011256d55"
        }
        response_example: >-
        {
        "supervisor_id": "supervisor-d73011256d55",
        "name": "test-in-plugins",
        "hostname": "dev-test3",
        "state": "ENABLED",
        "domain_id": "domain-1c5a6b8181ad",
        "tags": {
        "a": "b"
        },
        "labels": {},
        "created_at": "2022-06-15T06:27:51.904Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """
        desc: Disables a specific Supervisor. By changing the `state` parameter to `DISABLED`, the Supervisor cannot deploy or delete the `pod` of the plugin instance.
        note: ''
        request_example: >-
        {
        "supervisor_id": "supervisor-d73011256d55"
        }
        response_example: >-
        {
        "supervisor_id": "supervisor-d73011256d55",
        "name": "test-in-plugins",
        "hostname": "dev-test3",
        "state": "DISABLED",
        "domain_id": "domain-1c5a6b8181ad",
        "tags": {
        "a": "b"
        },
        "labels": {},
        "created_at": "2022-06-15T06:27:51.904Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def recover_plugin(self, request, context):
        """
        desc: Recovers a specific plugin instance in a specific Supervisor. Changes the `state` of the Supervisor to `RE-PROVISIONING`.
        note: ''
        request_example: >-
        {
        "supervisor_id": "supervisor-a4c287cba676",
        "plugin_id": "plugin-api-direct-mon-webhook",
        "version": "1.1.0"
        }
        response_example: >-
        {

        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        desc: Gets a list of all Supervisors. You can use a query to get a filtered list of Supervisors.
        note: ''
        request_example: >-
        {
        "query": {}
        }
        response_example: >-
        {
        "results": [
        {
        "supervisor_id": "supervisor-3a091f899539",
        "name": "root",
        "hostname": "dev-supervisor.svc.cluster.local",
        "state": "ENABLED",
        "is_public": true,
        "domain_id": "domain-1c5a6b8181ad",
        "labels": {},
        "created_at": "2020-05-12T00:24:48.250Z"
        },
        {
        "supervisor_id": "supervisor-a4c287cba676",
        "name": "test",
        "hostname": "dev-test",
        "state": "ENABLED",
        "domain_id": "domain-1c5a6b8181ad",
        "tags": {
        "a": "b"
        },
        "labels": {},
        "created_at": "2022-06-15T05:39:15.886Z"
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

    def list_plugins(self, request, context):
        """
        desc: Gets a list of all plugin instances regardless of Supervisors. Prints detailed information about the plugin instances, including `version`, `state`, and the relevant Supervisor.
        note: ''
        request_example: >-
        {
        "query": {}
        }
        response_example: >-
        {
        "results": [
        {
        "plugin_id": "plugin-openstack-inven-collector",
        "version": "0.4.1.20220609.122832",
        "state": "ACTIVE",
        "endpoint": "grpc://plugin-openstack-inven-collector-vbnnsoszfjsneiqz.dev-supervisor.svc.cluster.local:50051",
        "supervisor_id": "supervisor-3a091f899539",
        "supervisor_name": "root",
        "managed": true,
        "endpoints": [
        "grpc://172.16.16.234:50051"
        ]
        },
        {
        "plugin_id": "plugin-zabbix-mon-webhook",
        "version": "1.0",
        "state": "ACTIVE",
        "endpoint": "grpc://plugin-zabbix-mon-webhook-dgqqfqsqidieeuk.dev-supervisor.svc.cluster.local:50051",
        "supervisor_id": "supervisor-3a091f899539",
        "supervisor_name": "root",
        "managed": true,
        "endpoints": [
        "grpc://172.16.16.130:50051"
        ]
        }
        ],
        "total_count": 2
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SupervisorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'publish': grpc.unary_unary_rpc_method_handler(
                    servicer.publish,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PublishSupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'register': grpc.unary_unary_rpc_method_handler(
                    servicer.register,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'deregister': grpc.unary_unary_rpc_method_handler(
                    servicer.deregister,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'recover_plugin': grpc.unary_unary_rpc_method_handler(
                    servicer.recover_plugin,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RecoverPluginRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.GetSupervisorRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
            'list_plugins': grpc.unary_unary_rpc_method_handler(
                    servicer.list_plugins,
                    request_deserializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginsInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.plugin.v1.Supervisor', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Supervisor(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def publish(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/publish',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PublishSupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/register',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/update',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RegisterSupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/deregister',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/enable',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/disable',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def recover_plugin(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/recover_plugin',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.RecoverPluginRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/get',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.GetSupervisorRequest.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/list',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorQuery.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorsInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/stat',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.SupervisorStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def list_plugins(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.plugin.v1.Supervisor/list_plugins',
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginQuery.SerializeToString,
            spaceone_dot_api_dot_plugin_dot_v1_dot_supervisor__pb2.PluginsInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
