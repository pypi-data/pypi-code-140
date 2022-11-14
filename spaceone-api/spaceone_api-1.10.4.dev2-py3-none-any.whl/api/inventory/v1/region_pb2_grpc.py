# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.inventory.v1 import region_pb2 as spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2


class RegionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/create',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.CreateRegionRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/update',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.UpdateRegionRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/delete',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/get',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.GetRegionRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/list',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionsInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.inventory.v1.Region/stat',
                request_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class RegionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """
        desc: Creates a new Region. As the parameter `region_key`, which is automatically created when a Region is created, is in a form of `{provider}.{region_code}`, it is unique regardless of providers. You can also specify the latitude, longitude, and continent information in `tags`.
        request_example: >-
        {
        "name": "Asia Pacific (Seoul)",
        "region_code": "ap-northeast-2",
        "provider": "aws",
        "tags": {
        "continent": "asis_pacific",
        "longitude": "73.013805",
        "latitude": "19.147428"
        }
        }
        response_example: >-
        {
        "region_id": "region-e41deed3c939",
        "name": "Asia Pacific (Seoul)",
        "region_key": "aws.ap-northeast-2",
        "region_code": "ap-northeast-2",
        "provider": "aws",
        "tags": {
        "continent": "asia_pacific",
        "longitude": "73.013805",
        "latitude": "19.147428"
        },
        "domain_id": "domain-x1b3c34v432",
        "created_at": "2021-11-18T13:07:31.382Z",
        "updated_at": "2022-06-17T00:07:35.469Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        desc: Updates a specific Region. You can make changes in Region settings, including `name` and `tags`. The `tags` contain the continent, latitude, and longitude.
        request_example: >-
        {
        "region_id": "region-e41deed3c939",
        "name": "Region home",
        "tags": {
        "latitude": "6.34545",
        "continent": "asia_pacific",
        "longitude": "5.6433213"
        }
        }
        response_example: >-
        {
        "region_id": "region-e41deed3c939",
        "name": "Region home",
        "region_key": "aws.ap-northeast-2",
        "region_code": "ap-northeast-2",
        "provider": "aws",
        "tags": {
        "latitude": "6.34545",
        "continent": "asia_pacific",
        "longitude": "5.6433213"
        },
        "domain_id": "domain-x1b3c34v432",
        "created_at": "2021-11-18T13:07:31.382Z",
        "updated_at": "2022-06-17T00:07:35.469Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """
        desc: Deletes a specific Region. You must specify the `region_id` of the Region to delete.
        request_example: >-
        {
        "region_id": "region-e41deed3c939"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        desc: Gets a specific Region. Prints detailed information about the Region, including `name`, `region_code`, and a location coordinate.
        request_example: >-
        {
        "region_id": "region-f803eb00b567"
        }
        response_example: >-
        {
        "region_id": "region-f803eb00b567",
        "name": "Asia Pacific (Seoul)",
        "region_key": "aws.ap-northeast-2",
        "region_code": "ap-northeast-2",
        "provider": "aws",
        "tags": {
        "latitude": "6.34545",
        "continent": "asia_pacific",
        "longitude": "5.6433213"
        },
        "domain_id": "domain-x1b3c34v432",
        "created_at": "2022-03-21T09:08:31.961Z",
        "updated_at": "2022-06-17T00:07:35.749Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        desc: Gets a list of all Regions. You can use a query to get a filtered list of Regions.
        request_example: >-
        {
        "query": {
        "filter": [
        {
        "key": "name",
        "value": "Asia Pacific",
        "operator": "contain"
        }
        ]
        }
        }
        response_example: >-
        {
        "results": [
        {
        "region_id": "region-e41deed3c939",
        "name": "Asia Pacific (Mumbai)",
        "region_key": "aws.ap-south-1",
        "region_code": "ap-south-1",
        "provider": "aws",
        "tags": {
        "continent": "asia_pacific",
        "longitude": "73.013805",
        "latitude": "19.147428"
        },
        "domain_id": "domain-x1b3c34v432",
        "created_at": "2021-11-18T13:07:31.382Z",
        "updated_at": "2022-06-17T00:07:35.469Z"
        },
        {
        "region_id": "region-f803eb00b567",
        "name": "Asia Pacific (Seoul)",
        "region_key": "aws.ap-northeast-2",
        "region_code": "ap-northeast-2",
        "provider": "aws",
        "tags": {
        "latitude": "6.34545",
        "continent": "asia_pacific",
        "longitude": "5.6433213"
        },
        "domain_id": "domain-x1b3c34v432",
        "created_at": "2022-03-21T09:08:31.961Z",
        "updated_at": "2022-06-17T00:07:35.749Z"
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


def add_RegionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.CreateRegionRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.UpdateRegionRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.GetRegionRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.inventory.v1.Region', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Region(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/create',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.CreateRegionRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/update',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.UpdateRegionRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/delete',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/get',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.GetRegionRequest.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/list',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionQuery.SerializeToString,
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionsInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.inventory.v1.Region/stat',
            spaceone_dot_api_dot_inventory_dot_v1_dot_region__pb2.RegionStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
