# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.notification.v1 import notification_usage_pb2 as spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2


class NotificationUsageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.list = channel.unary_unary(
                '/spaceone.api.notification.v1.NotificationUsage/list',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsagesInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.notification.v1.NotificationUsage/stat',
                request_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class NotificationUsageServicer(object):
    """Missing associated documentation comment in .proto file."""

    def list(self, request, context):
        """
        desc: Gets a list of all NotificationUsages. You can use a query to get a filtered list of Notification Usages.
        request_example: >-
        {
        "query": {}
        }
        response_example: >-
        {
        "results": [
        {
        "protocol_id": "protocol-123456789012",
        "usage_date": "08",
        "usage_month": "2022-05",
        "count": 2,
        "domain_id": "domain-123456789012"
        },
        {
        "protocol_id": "protocol-123456789012",
        "usage_date": "18",
        "usage_month": "2022-05",
        "count": 7,
        "domain_id": "domain-123456789012"
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


def add_NotificationUsageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsagesInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.notification.v1.NotificationUsage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class NotificationUsage(object):
    """Missing associated documentation comment in .proto file."""

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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.NotificationUsage/list',
            spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageQuery.SerializeToString,
            spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsagesInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.notification.v1.NotificationUsage/stat',
            spaceone_dot_api_dot_notification_dot_v1_dot_notification__usage__pb2.NotificationUsageStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
