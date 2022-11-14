# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from feast.core import CoreService_pb2 as feast_dot_core_dot_CoreService__pb2


class CoreServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetFeastCoreVersion = channel.unary_unary(
                '/feast.core.CoreService/GetFeastCoreVersion',
                request_serializer=feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionResponse.FromString,
                )
        self.GetEntity = channel.unary_unary(
                '/feast.core.CoreService/GetEntity',
                request_serializer=feast_dot_core_dot_CoreService__pb2.GetEntityRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.GetEntityResponse.FromString,
                )
        self.ListFeatures = channel.unary_unary(
                '/feast.core.CoreService/ListFeatures',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ListFeaturesRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ListFeaturesResponse.FromString,
                )
        self.ApplyEntity = channel.unary_unary(
                '/feast.core.CoreService/ApplyEntity',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ApplyEntityRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ApplyEntityResponse.FromString,
                )
        self.ListEntities = channel.unary_unary(
                '/feast.core.CoreService/ListEntities',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ListEntitiesRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ListEntitiesResponse.FromString,
                )
        self.CreateProject = channel.unary_unary(
                '/feast.core.CoreService/CreateProject',
                request_serializer=feast_dot_core_dot_CoreService__pb2.CreateProjectRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.CreateProjectResponse.FromString,
                )
        self.ArchiveProject = channel.unary_unary(
                '/feast.core.CoreService/ArchiveProject',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ArchiveProjectRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ArchiveProjectResponse.FromString,
                )
        self.ListProjects = channel.unary_unary(
                '/feast.core.CoreService/ListProjects',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ListProjectsRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ListProjectsResponse.FromString,
                )
        self.ApplyFeatureTable = channel.unary_unary(
                '/feast.core.CoreService/ApplyFeatureTable',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableResponse.FromString,
                )
        self.ListFeatureTables = channel.unary_unary(
                '/feast.core.CoreService/ListFeatureTables',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ListFeatureTablesRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ListFeatureTablesResponse.FromString,
                )
        self.GetFeatureTable = channel.unary_unary(
                '/feast.core.CoreService/GetFeatureTable',
                request_serializer=feast_dot_core_dot_CoreService__pb2.GetFeatureTableRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.GetFeatureTableResponse.FromString,
                )
        self.DeleteFeatureTable = channel.unary_unary(
                '/feast.core.CoreService/DeleteFeatureTable',
                request_serializer=feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableResponse.FromString,
                )
        self.ListOnlineStores = channel.unary_unary(
                '/feast.core.CoreService/ListOnlineStores',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ListOnlineStoresRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ListOnlineStoresResponse.FromString,
                )
        self.GetOnlineStore = channel.unary_unary(
                '/feast.core.CoreService/GetOnlineStore',
                request_serializer=feast_dot_core_dot_CoreService__pb2.GetOnlineStoreRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.GetOnlineStoreResponse.FromString,
                )
        self.RegisterOnlineStore = channel.unary_unary(
                '/feast.core.CoreService/RegisterOnlineStore',
                request_serializer=feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreResponse.FromString,
                )
        self.ArchiveOnlineStore = channel.unary_unary(
                '/feast.core.CoreService/ArchiveOnlineStore',
                request_serializer=feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreRequest.SerializeToString,
                response_deserializer=feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreResponse.FromString,
                )


class CoreServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetFeastCoreVersion(self, request, context):
        """Retrieve version information about this Feast deployment
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetEntity(self, request, context):
        """Returns a specific entity
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFeatures(self, request, context):
        """Returns all feature references and respective features matching that filter. If none are found
        an empty map will be returned
        If no filter is provided in the request, the response will contain all the features
        currently stored in the default project.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplyEntity(self, request, context):
        """Create or update and existing entity.

        This function is idempotent - it will not create a new entity if schema does not change.
        Schema changes will update the entity if the changes are valid.
        Following changes are not valid:
        - Changes to name
        - Changes to type
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListEntities(self, request, context):
        """Returns all entity references and respective entities matching that filter. If none are found
        an empty map will be returned
        If no filter is provided in the request, the response will contain all the entities
        currently stored in the default project.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateProject(self, request, context):
        """Creates a project. Projects serve as namespaces within which resources like features will be
        created. Feature table names as must be unique within a project while field (Feature/Entity) names
        must be unique within a Feature Table. Project names themselves must be globally unique.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ArchiveProject(self, request, context):
        """Archives a project. Archived projects will continue to exist and function, but won't be visible
        through the Core API. Any existing ingestion or serving requests will continue to function,
        but will result in warning messages being logged. It is not possible to unarchive a project
        through the Core API
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListProjects(self, request, context):
        """Lists all projects active projects.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ApplyFeatureTable(self, request, context):
        """Feature Tables 

        Create or update an existing feature table.
        This function is idempotent - it will not create a new feature table if the schema does not change.
        Schema changes will update the feature table if the changes are valid.
        All changes except the following are valid:
        - Changes to feature table name.
        - Changes to entities
        - Changes to feature name and type
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFeatureTables(self, request, context):
        """List feature tables that match a given filter.
        Returns the references of the Feature Tables matching that filter. If none are found,
        an empty list will be returned.
        If no filter is provided in the request, the response will match all the feature
        tables currently stored in the registry.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFeatureTable(self, request, context):
        """Returns a specific feature table
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFeatureTable(self, request, context):
        """Delete a specific feature table
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListOnlineStores(self, request, context):
        """Lists all online stores
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetOnlineStore(self, request, context):
        """Returns a specific online stores
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterOnlineStore(self, request, context):
        """Registers new online store to feast core
        or updates properties for existing online store
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ArchiveOnlineStore(self, request, context):
        """Archives an online store to mark it deprecated
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CoreServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetFeastCoreVersion': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFeastCoreVersion,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionResponse.SerializeToString,
            ),
            'GetEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.GetEntity,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.GetEntityRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.GetEntityResponse.SerializeToString,
            ),
            'ListFeatures': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFeatures,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ListFeaturesRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ListFeaturesResponse.SerializeToString,
            ),
            'ApplyEntity': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyEntity,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ApplyEntityRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ApplyEntityResponse.SerializeToString,
            ),
            'ListEntities': grpc.unary_unary_rpc_method_handler(
                    servicer.ListEntities,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ListEntitiesRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ListEntitiesResponse.SerializeToString,
            ),
            'CreateProject': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateProject,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.CreateProjectRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.CreateProjectResponse.SerializeToString,
            ),
            'ArchiveProject': grpc.unary_unary_rpc_method_handler(
                    servicer.ArchiveProject,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ArchiveProjectRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ArchiveProjectResponse.SerializeToString,
            ),
            'ListProjects': grpc.unary_unary_rpc_method_handler(
                    servicer.ListProjects,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ListProjectsRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ListProjectsResponse.SerializeToString,
            ),
            'ApplyFeatureTable': grpc.unary_unary_rpc_method_handler(
                    servicer.ApplyFeatureTable,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableResponse.SerializeToString,
            ),
            'ListFeatureTables': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFeatureTables,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ListFeatureTablesRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ListFeatureTablesResponse.SerializeToString,
            ),
            'GetFeatureTable': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFeatureTable,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.GetFeatureTableRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.GetFeatureTableResponse.SerializeToString,
            ),
            'DeleteFeatureTable': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFeatureTable,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableResponse.SerializeToString,
            ),
            'ListOnlineStores': grpc.unary_unary_rpc_method_handler(
                    servicer.ListOnlineStores,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ListOnlineStoresRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ListOnlineStoresResponse.SerializeToString,
            ),
            'GetOnlineStore': grpc.unary_unary_rpc_method_handler(
                    servicer.GetOnlineStore,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.GetOnlineStoreRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.GetOnlineStoreResponse.SerializeToString,
            ),
            'RegisterOnlineStore': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterOnlineStore,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreResponse.SerializeToString,
            ),
            'ArchiveOnlineStore': grpc.unary_unary_rpc_method_handler(
                    servicer.ArchiveOnlineStore,
                    request_deserializer=feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreRequest.FromString,
                    response_serializer=feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'feast.core.CoreService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CoreService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetFeastCoreVersion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/GetFeastCoreVersion',
            feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.GetFeastCoreVersionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/GetEntity',
            feast_dot_core_dot_CoreService__pb2.GetEntityRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.GetEntityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFeatures(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ListFeatures',
            feast_dot_core_dot_CoreService__pb2.ListFeaturesRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ListFeaturesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ApplyEntity(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ApplyEntity',
            feast_dot_core_dot_CoreService__pb2.ApplyEntityRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ApplyEntityResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListEntities(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ListEntities',
            feast_dot_core_dot_CoreService__pb2.ListEntitiesRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ListEntitiesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/CreateProject',
            feast_dot_core_dot_CoreService__pb2.CreateProjectRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.CreateProjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ArchiveProject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ArchiveProject',
            feast_dot_core_dot_CoreService__pb2.ArchiveProjectRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ArchiveProjectResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListProjects(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ListProjects',
            feast_dot_core_dot_CoreService__pb2.ListProjectsRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ListProjectsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ApplyFeatureTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ApplyFeatureTable',
            feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ApplyFeatureTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFeatureTables(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ListFeatureTables',
            feast_dot_core_dot_CoreService__pb2.ListFeatureTablesRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ListFeatureTablesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFeatureTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/GetFeatureTable',
            feast_dot_core_dot_CoreService__pb2.GetFeatureTableRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.GetFeatureTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteFeatureTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/DeleteFeatureTable',
            feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.DeleteFeatureTableResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListOnlineStores(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ListOnlineStores',
            feast_dot_core_dot_CoreService__pb2.ListOnlineStoresRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ListOnlineStoresResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetOnlineStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/GetOnlineStore',
            feast_dot_core_dot_CoreService__pb2.GetOnlineStoreRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.GetOnlineStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterOnlineStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/RegisterOnlineStore',
            feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.RegisterOnlineStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ArchiveOnlineStore(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/feast.core.CoreService/ArchiveOnlineStore',
            feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreRequest.SerializeToString,
            feast_dot_core_dot_CoreService__pb2.ArchiveOnlineStoreResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
