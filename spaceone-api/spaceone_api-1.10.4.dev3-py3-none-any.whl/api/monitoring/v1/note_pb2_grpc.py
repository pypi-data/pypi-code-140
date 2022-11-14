# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.monitoring.v1 import note_pb2 as spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2


class NoteStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/create',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.CreateNoteRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
                )
        self.update = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/update',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.UpdateNoteRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
                )
        self.delete = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/delete',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.get = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/get',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.GetNoteRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
                )
        self.list = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/list',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NotesInfo.FromString,
                )
        self.stat = channel.unary_unary(
                '/spaceone.api.monitoring.v1.Note/stat',
                request_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                )


class NoteServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """
        desc: Creates a new Note. You can create Notes for each Alert to record the information needed to manage the Alerts.
        request_example: >-
        {
        "alert_id": "alert-160ce04f6908",
        "note": "This is a description",
        "domain_id": "domain-58010aa2e451"
        }
        response_example: >-
        {
        "note_id": "note-df107d31bf20",
        "alert_id": "alert-160ce04f6908",
        "note": "This is a description",
        "created_by": "seolmin@mz.co.kr",
        "project_id": "project-52a423012d5e",
        "domain_id": "domain-58010aa2e451",
        "created_at": "2022-06-29T08:26:14.418Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """
        desc: Updates a specific Note. You must specify the `note_id` for Note validation check. If the Note exists, it is updated.
        request_example: >-
        {
        "note_id": "note-df107d31bf20",
        "note": "This is a test",
        "domain_id": "domain-58010aa2e451"
        }
        response_example: >-
        {
        "note_id": "note-df107d31bf20",
        "alert_id": "alert-160ce04f6908",
        "note": "This is a test",
        "created_by": "seolmin@mz.co.kr",
        "project_id": "project-52a423012d5e",
        "domain_id": "domain-58010aa2e451",
        "created_at": "2022-06-29T08:26:14.418Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """
        desc: Deletes a specific Note. You must specify the `note_id` of the Note to delete.
        request_example: >-
        {
        "note_id": "note-0bfac585bf5a",
        "domain_id": "domain-58010aa2e451"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """
        desc: Gets a specific Note. You must specify the `note_id` and `domain_id`.
        request_example: >-
        {
        "note_id": "note-0bfac585bf5a",
        "domain_id": "domain-58010aa2e451"
        }
        response_example: >-
        {
        "note_id": "note-0bfac585bf5a",
        "alert_id": "alert-fbfd78e43df8",
        "note": "test",
        "created_by": "hykang@mz.co.kr",
        "project_id": "project-52a423012d5e",
        "domain_id": "domain-58010aa2e451",
        "created_at": "2022-06-23T09:52:42.251Z"
        }
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """
        desc: Gets a list of all Notes. You can use a query to get a filtered list of Notes.
        request_example: >-
        {
        "query": {},
        "domain_id": "domain-58010aa2e451"
        }
        response_example: >-
        {
        "results": [
        {
        "note_id": "note-0597bd748be0",
        "alert_id": "alert-fbfd78e43df8",
        "note": "http://spaceone.org",
        "created_by": "hykang@mz.co.kr",
        "project_id": "project-52a423012d5e",
        "domain_id": "domain-58010aa2e451",
        "created_at": "2022-06-23T09:58:23.838Z"
        },
        {
        "note_id": "note-0bfac585bf5a",
        "alert_id": "alert-fbfd78e43df8",
        "note": "test",
        "created_by": "hykang@mz.co.kr",
        "project_id": "project-52a423012d5e",
        "domain_id": "domain-58010aa2e451",
        "created_at": "2022-06-23T09:52:42.251Z"
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


def add_NoteServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.CreateNoteRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.UpdateNoteRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.GetNoteRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NotesInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.monitoring.v1.Note', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Note(object):
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/create',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.CreateNoteRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/update',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.UpdateNoteRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/delete',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteRequest.SerializeToString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/get',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.GetNoteRequest.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/list',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteQuery.SerializeToString,
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NotesInfo.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/spaceone.api.monitoring.v1.Note/stat',
            spaceone_dot_api_dot_monitoring_dot_v1_dot_note__pb2.NoteStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
