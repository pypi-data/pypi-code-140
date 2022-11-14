# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2
from yandex.cloud.vpc.v1 import gateway_pb2 as yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__pb2
from yandex.cloud.vpc.v1 import gateway_service_pb2 as yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2


class GatewayServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/Get',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.GetGatewayRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__pb2.Gateway.FromString,
                )
        self.List = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/List',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/Create',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.CreateGatewayRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.Update = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/Update',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.UpdateGatewayRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.Delete = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/Delete',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.DeleteGatewayRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.ListOperations = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/ListOperations',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsResponse.FromString,
                )
        self.Move = channel.unary_unary(
                '/yandex.cloud.vpc.v1.GatewayService/Move',
                request_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.MoveGatewayRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )


class GatewayServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Returns the specified Gateway resource.

        To get the list of all available Gateway resources, make a [List] request.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """Retrieves the list of Gateway resources in the specified folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Creates a gateway in the specified folder.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Updates the specified gateway.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Deletes the specified gateway.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOperations(self, request, context):
        """List operations for the specified gateway.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Move(self, request, context):
        """Move a gateway to another folder
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GatewayServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.GetGatewayRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__pb2.Gateway.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.CreateGatewayRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.UpdateGatewayRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.DeleteGatewayRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'ListOperations': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOperations,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsResponse.SerializeToString,
            ),
            'Move': grpc.unary_unary_rpc_method_handler(
                    servicer.Move,
                    request_deserializer=yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.MoveGatewayRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.vpc.v1.GatewayService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GatewayService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/Get',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.GetGatewayRequest.SerializeToString,
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__pb2.Gateway.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/List',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysRequest.SerializeToString,
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewaysResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/Create',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.CreateGatewayRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/Update',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.UpdateGatewayRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/Delete',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.DeleteGatewayRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListOperations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/ListOperations',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsRequest.SerializeToString,
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.ListGatewayOperationsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Move(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.vpc.v1.GatewayService/Move',
            yandex_dot_cloud_dot_vpc_dot_v1_dot_gateway__service__pb2.MoveGatewayRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
