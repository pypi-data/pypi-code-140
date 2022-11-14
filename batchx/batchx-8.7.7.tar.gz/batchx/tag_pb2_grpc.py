# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import tag_pb2 as tag__pb2


class TagServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetTag = channel.unary_unary(
                '/batchx.tag.TagService/GetTag',
                request_serializer=tag__pb2.GetTagRequest.SerializeToString,
                response_deserializer=tag__pb2.GetTagResponse.FromString,
                )
        self.ListEnvironmentTags = channel.unary_unary(
                '/batchx.tag.TagService/ListEnvironmentTags',
                request_serializer=tag__pb2.ListEnvironmentTagsRequest.SerializeToString,
                response_deserializer=tag__pb2.ListEnvironmentTagsResponse.FromString,
                )
        self.CreateTag = channel.unary_unary(
                '/batchx.tag.TagService/CreateTag',
                request_serializer=tag__pb2.CreateTagRequest.SerializeToString,
                response_deserializer=tag__pb2.CreateTagResponse.FromString,
                )
        self.DisableTag = channel.unary_unary(
                '/batchx.tag.TagService/DisableTag',
                request_serializer=tag__pb2.DisableTagRequest.SerializeToString,
                response_deserializer=tag__pb2.DisableTagResponse.FromString,
                )
        self.DeleteTag = channel.unary_unary(
                '/batchx.tag.TagService/DeleteTag',
                request_serializer=tag__pb2.DeleteTagRequest.SerializeToString,
                response_deserializer=tag__pb2.DeleteTagResponse.FromString,
                )
        self.UpdateTag = channel.unary_unary(
                '/batchx.tag.TagService/UpdateTag',
                request_serializer=tag__pb2.UpdateTagRequest.SerializeToString,
                response_deserializer=tag__pb2.UpdateTagResponse.FromString,
                )


class TagServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEnvironmentTags(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisableTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateTag(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TagServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetTag': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTag,
                    request_deserializer=tag__pb2.GetTagRequest.FromString,
                    response_serializer=tag__pb2.GetTagResponse.SerializeToString,
            ),
            'ListEnvironmentTags': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEnvironmentTags,
                    request_deserializer=tag__pb2.ListEnvironmentTagsRequest.FromString,
                    response_serializer=tag__pb2.ListEnvironmentTagsResponse.SerializeToString,
            ),
            'CreateTag': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTag,
                    request_deserializer=tag__pb2.CreateTagRequest.FromString,
                    response_serializer=tag__pb2.CreateTagResponse.SerializeToString,
            ),
            'DisableTag': grpc.unary_unary_rpc_method_handler(
                    servicer.DisableTag,
                    request_deserializer=tag__pb2.DisableTagRequest.FromString,
                    response_serializer=tag__pb2.DisableTagResponse.SerializeToString,
            ),
            'DeleteTag': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteTag,
                    request_deserializer=tag__pb2.DeleteTagRequest.FromString,
                    response_serializer=tag__pb2.DeleteTagResponse.SerializeToString,
            ),
            'UpdateTag': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateTag,
                    request_deserializer=tag__pb2.UpdateTagRequest.FromString,
                    response_serializer=tag__pb2.UpdateTagResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'batchx.tag.TagService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TagService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/GetTag',
            tag__pb2.GetTagRequest.SerializeToString,
            tag__pb2.GetTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEnvironmentTags(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/ListEnvironmentTags',
            tag__pb2.ListEnvironmentTagsRequest.SerializeToString,
            tag__pb2.ListEnvironmentTagsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/CreateTag',
            tag__pb2.CreateTagRequest.SerializeToString,
            tag__pb2.CreateTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisableTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/DisableTag',
            tag__pb2.DisableTagRequest.SerializeToString,
            tag__pb2.DisableTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/DeleteTag',
            tag__pb2.DeleteTagRequest.SerializeToString,
            tag__pb2.DeleteTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateTag(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/batchx.tag.TagService/UpdateTag',
            tag__pb2.UpdateTagRequest.SerializeToString,
            tag__pb2.UpdateTagResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
