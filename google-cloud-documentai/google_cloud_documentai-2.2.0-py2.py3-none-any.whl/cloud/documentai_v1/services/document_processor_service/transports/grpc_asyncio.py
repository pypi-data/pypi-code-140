# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from typing import Awaitable, Callable, Dict, Optional, Sequence, Tuple, Union
import warnings

from google.api_core import gapic_v1, grpc_helpers_async, operations_v1
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.cloud.location import locations_pb2  # type: ignore
from google.longrunning import operations_pb2  # type: ignore
import grpc  # type: ignore
from grpc.experimental import aio  # type: ignore

from google.cloud.documentai_v1.types import document_processor_service
from google.cloud.documentai_v1.types import processor
from google.cloud.documentai_v1.types import processor as gcd_processor

from .base import DEFAULT_CLIENT_INFO, DocumentProcessorServiceTransport
from .grpc import DocumentProcessorServiceGrpcTransport


class DocumentProcessorServiceGrpcAsyncIOTransport(DocumentProcessorServiceTransport):
    """gRPC AsyncIO backend transport for DocumentProcessorService.

    Service to call Cloud DocumentAI to process documents
    according to the processor's definition. Processors are built
    using state-of-the-art Google AI such as natural language,
    computer vision, and translation to extract structured
    information from unstructured or semi-structured documents.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """

    _grpc_channel: aio.Channel
    _stubs: Dict[str, Callable] = {}

    @classmethod
    def create_channel(
        cls,
        host: str = "documentai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        quota_project_id: Optional[str] = None,
        **kwargs,
    ) -> aio.Channel:
        """Create and return a gRPC AsyncIO channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            aio.Channel: A gRPC AsyncIO channel object.
        """

        return grpc_helpers_async.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs,
        )

    def __init__(
        self,
        *,
        host: str = "documentai.googleapis.com",
        credentials: Optional[ga_credentials.Credentials] = None,
        credentials_file: Optional[str] = None,
        scopes: Optional[Sequence[str]] = None,
        channel: Optional[aio.Channel] = None,
        api_mtls_endpoint: Optional[str] = None,
        client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
        client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            channel (Optional[aio.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
            google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsAsyncClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None
        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @property
    def grpc_channel(self) -> aio.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsAsyncClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsAsyncClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def process_document(
        self,
    ) -> Callable[
        [document_processor_service.ProcessRequest],
        Awaitable[document_processor_service.ProcessResponse],
    ]:
        r"""Return a callable for the process document method over gRPC.

        Processes a single document.

        Returns:
            Callable[[~.ProcessRequest],
                    Awaitable[~.ProcessResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "process_document" not in self._stubs:
            self._stubs["process_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/ProcessDocument",
                request_serializer=document_processor_service.ProcessRequest.serialize,
                response_deserializer=document_processor_service.ProcessResponse.deserialize,
            )
        return self._stubs["process_document"]

    @property
    def batch_process_documents(
        self,
    ) -> Callable[
        [document_processor_service.BatchProcessRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the batch process documents method over gRPC.

        LRO endpoint to batch process many documents. The output is
        written to Cloud Storage as JSON in the [Document] format.

        Returns:
            Callable[[~.BatchProcessRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "batch_process_documents" not in self._stubs:
            self._stubs["batch_process_documents"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/BatchProcessDocuments",
                request_serializer=document_processor_service.BatchProcessRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["batch_process_documents"]

    @property
    def fetch_processor_types(
        self,
    ) -> Callable[
        [document_processor_service.FetchProcessorTypesRequest],
        Awaitable[document_processor_service.FetchProcessorTypesResponse],
    ]:
        r"""Return a callable for the fetch processor types method over gRPC.

        Fetches processor types. Note that we do not use
        ListProcessorTypes here because it is not paginated.

        Returns:
            Callable[[~.FetchProcessorTypesRequest],
                    Awaitable[~.FetchProcessorTypesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "fetch_processor_types" not in self._stubs:
            self._stubs["fetch_processor_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/FetchProcessorTypes",
                request_serializer=document_processor_service.FetchProcessorTypesRequest.serialize,
                response_deserializer=document_processor_service.FetchProcessorTypesResponse.deserialize,
            )
        return self._stubs["fetch_processor_types"]

    @property
    def list_processor_types(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorTypesRequest],
        Awaitable[document_processor_service.ListProcessorTypesResponse],
    ]:
        r"""Return a callable for the list processor types method over gRPC.

        Lists the processor types that exist.

        Returns:
            Callable[[~.ListProcessorTypesRequest],
                    Awaitable[~.ListProcessorTypesResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_processor_types" not in self._stubs:
            self._stubs["list_processor_types"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/ListProcessorTypes",
                request_serializer=document_processor_service.ListProcessorTypesRequest.serialize,
                response_deserializer=document_processor_service.ListProcessorTypesResponse.deserialize,
            )
        return self._stubs["list_processor_types"]

    @property
    def list_processors(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorsRequest],
        Awaitable[document_processor_service.ListProcessorsResponse],
    ]:
        r"""Return a callable for the list processors method over gRPC.

        Lists all processors which belong to this project.

        Returns:
            Callable[[~.ListProcessorsRequest],
                    Awaitable[~.ListProcessorsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_processors" not in self._stubs:
            self._stubs["list_processors"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/ListProcessors",
                request_serializer=document_processor_service.ListProcessorsRequest.serialize,
                response_deserializer=document_processor_service.ListProcessorsResponse.deserialize,
            )
        return self._stubs["list_processors"]

    @property
    def get_processor(
        self,
    ) -> Callable[
        [document_processor_service.GetProcessorRequest], Awaitable[processor.Processor]
    ]:
        r"""Return a callable for the get processor method over gRPC.

        Gets a processor detail.

        Returns:
            Callable[[~.GetProcessorRequest],
                    Awaitable[~.Processor]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_processor" not in self._stubs:
            self._stubs["get_processor"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/GetProcessor",
                request_serializer=document_processor_service.GetProcessorRequest.serialize,
                response_deserializer=processor.Processor.deserialize,
            )
        return self._stubs["get_processor"]

    @property
    def get_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.GetProcessorVersionRequest],
        Awaitable[processor.ProcessorVersion],
    ]:
        r"""Return a callable for the get processor version method over gRPC.

        Gets a processor version detail.

        Returns:
            Callable[[~.GetProcessorVersionRequest],
                    Awaitable[~.ProcessorVersion]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_processor_version" not in self._stubs:
            self._stubs["get_processor_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/GetProcessorVersion",
                request_serializer=document_processor_service.GetProcessorVersionRequest.serialize,
                response_deserializer=processor.ProcessorVersion.deserialize,
            )
        return self._stubs["get_processor_version"]

    @property
    def list_processor_versions(
        self,
    ) -> Callable[
        [document_processor_service.ListProcessorVersionsRequest],
        Awaitable[document_processor_service.ListProcessorVersionsResponse],
    ]:
        r"""Return a callable for the list processor versions method over gRPC.

        Lists all versions of a processor.

        Returns:
            Callable[[~.ListProcessorVersionsRequest],
                    Awaitable[~.ListProcessorVersionsResponse]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_processor_versions" not in self._stubs:
            self._stubs["list_processor_versions"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/ListProcessorVersions",
                request_serializer=document_processor_service.ListProcessorVersionsRequest.serialize,
                response_deserializer=document_processor_service.ListProcessorVersionsResponse.deserialize,
            )
        return self._stubs["list_processor_versions"]

    @property
    def delete_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.DeleteProcessorVersionRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete processor version method over gRPC.

        Deletes the processor version, all artifacts under
        the processor version will be deleted.

        Returns:
            Callable[[~.DeleteProcessorVersionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_processor_version" not in self._stubs:
            self._stubs["delete_processor_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/DeleteProcessorVersion",
                request_serializer=document_processor_service.DeleteProcessorVersionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_processor_version"]

    @property
    def deploy_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.DeployProcessorVersionRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the deploy processor version method over gRPC.

        Deploys the processor version.

        Returns:
            Callable[[~.DeployProcessorVersionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "deploy_processor_version" not in self._stubs:
            self._stubs["deploy_processor_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/DeployProcessorVersion",
                request_serializer=document_processor_service.DeployProcessorVersionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["deploy_processor_version"]

    @property
    def undeploy_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.UndeployProcessorVersionRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the undeploy processor version method over gRPC.

        Undeploys the processor version.

        Returns:
            Callable[[~.UndeployProcessorVersionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "undeploy_processor_version" not in self._stubs:
            self._stubs["undeploy_processor_version"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/UndeployProcessorVersion",
                request_serializer=document_processor_service.UndeployProcessorVersionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["undeploy_processor_version"]

    @property
    def create_processor(
        self,
    ) -> Callable[
        [document_processor_service.CreateProcessorRequest],
        Awaitable[gcd_processor.Processor],
    ]:
        r"""Return a callable for the create processor method over gRPC.

        Creates a processor from the type processor that the
        user chose. The processor will be at "ENABLED" state by
        default after its creation.

        Returns:
            Callable[[~.CreateProcessorRequest],
                    Awaitable[~.Processor]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "create_processor" not in self._stubs:
            self._stubs["create_processor"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/CreateProcessor",
                request_serializer=document_processor_service.CreateProcessorRequest.serialize,
                response_deserializer=gcd_processor.Processor.deserialize,
            )
        return self._stubs["create_processor"]

    @property
    def delete_processor(
        self,
    ) -> Callable[
        [document_processor_service.DeleteProcessorRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the delete processor method over gRPC.

        Deletes the processor, unloads all deployed model
        artifacts if it was enabled and then deletes all
        artifacts associated with this processor.

        Returns:
            Callable[[~.DeleteProcessorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_processor" not in self._stubs:
            self._stubs["delete_processor"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/DeleteProcessor",
                request_serializer=document_processor_service.DeleteProcessorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["delete_processor"]

    @property
    def enable_processor(
        self,
    ) -> Callable[
        [document_processor_service.EnableProcessorRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the enable processor method over gRPC.

        Enables a processor

        Returns:
            Callable[[~.EnableProcessorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "enable_processor" not in self._stubs:
            self._stubs["enable_processor"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/EnableProcessor",
                request_serializer=document_processor_service.EnableProcessorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["enable_processor"]

    @property
    def disable_processor(
        self,
    ) -> Callable[
        [document_processor_service.DisableProcessorRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the disable processor method over gRPC.

        Disables a processor

        Returns:
            Callable[[~.DisableProcessorRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "disable_processor" not in self._stubs:
            self._stubs["disable_processor"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/DisableProcessor",
                request_serializer=document_processor_service.DisableProcessorRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["disable_processor"]

    @property
    def set_default_processor_version(
        self,
    ) -> Callable[
        [document_processor_service.SetDefaultProcessorVersionRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the set default processor version method over gRPC.

        Set the default (active) version of a
        [Processor][google.cloud.documentai.v1.Processor] that will be
        used in
        [ProcessDocument][google.cloud.documentai.v1.DocumentProcessorService.ProcessDocument]
        and
        [BatchProcessDocuments][google.cloud.documentai.v1.DocumentProcessorService.BatchProcessDocuments].

        Returns:
            Callable[[~.SetDefaultProcessorVersionRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_default_processor_version" not in self._stubs:
            self._stubs[
                "set_default_processor_version"
            ] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/SetDefaultProcessorVersion",
                request_serializer=document_processor_service.SetDefaultProcessorVersionRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["set_default_processor_version"]

    @property
    def review_document(
        self,
    ) -> Callable[
        [document_processor_service.ReviewDocumentRequest],
        Awaitable[operations_pb2.Operation],
    ]:
        r"""Return a callable for the review document method over gRPC.

        Send a document for Human Review. The input document
        should be processed by the specified processor.

        Returns:
            Callable[[~.ReviewDocumentRequest],
                    Awaitable[~.Operation]]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "review_document" not in self._stubs:
            self._stubs["review_document"] = self.grpc_channel.unary_unary(
                "/google.cloud.documentai.v1.DocumentProcessorService/ReviewDocument",
                request_serializer=document_processor_service.ReviewDocumentRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["review_document"]

    def close(self):
        return self.grpc_channel.close()

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[
        [operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse
    ]:
        r"""Return a callable for the list_operations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[
        [locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse
    ]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC."""
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]


__all__ = ("DocumentProcessorServiceGrpcAsyncIOTransport",)
