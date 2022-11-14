# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from yandex.cloud.dataproc.v1 import job_pb2 as yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2
from yandex.cloud.dataproc.v1 import job_service_pb2 as yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2
from yandex.cloud.operation import operation_pb2 as yandex_dot_cloud_dot_operation_dot_operation__pb2


class JobServiceStub(object):
    """A set of methods for managing Data Proc jobs.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.List = channel.unary_unary(
                '/yandex.cloud.dataproc.v1.JobService/List',
                request_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/yandex.cloud.dataproc.v1.JobService/Create',
                request_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CreateJobRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )
        self.Get = channel.unary_unary(
                '/yandex.cloud.dataproc.v1.JobService/Get',
                request_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.GetJobRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2.Job.FromString,
                )
        self.ListLog = channel.unary_unary(
                '/yandex.cloud.dataproc.v1.JobService/ListLog',
                request_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogResponse.FromString,
                )
        self.Cancel = channel.unary_unary(
                '/yandex.cloud.dataproc.v1.JobService/Cancel',
                request_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CancelJobRequest.SerializeToString,
                response_deserializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
                )


class JobServiceServicer(object):
    """A set of methods for managing Data Proc jobs.
    """

    def List(self, request, context):
        """Retrieves a list of jobs for a cluster.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Creates a job for a cluster.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Returns the specified job.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListLog(self, request, context):
        """Returns a log for specified job.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Cancel(self, request, context):
        """Cancels the specified Dataproc job.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JobServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CreateJobRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.GetJobRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2.Job.SerializeToString,
            ),
            'ListLog': grpc.unary_unary_rpc_method_handler(
                    servicer.ListLog,
                    request_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogResponse.SerializeToString,
            ),
            'Cancel': grpc.unary_unary_rpc_method_handler(
                    servicer.Cancel,
                    request_deserializer=yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CancelJobRequest.FromString,
                    response_serializer=yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'yandex.cloud.dataproc.v1.JobService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class JobService(object):
    """A set of methods for managing Data Proc jobs.
    """

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
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.dataproc.v1.JobService/List',
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsRequest.SerializeToString,
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobsResponse.FromString,
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
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.dataproc.v1.JobService/Create',
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CreateJobRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

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
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.dataproc.v1.JobService/Get',
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.GetJobRequest.SerializeToString,
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__pb2.Job.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListLog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.dataproc.v1.JobService/ListLog',
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogRequest.SerializeToString,
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.ListJobLogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Cancel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/yandex.cloud.dataproc.v1.JobService/Cancel',
            yandex_dot_cloud_dot_dataproc_dot_v1_dot_job__service__pb2.CancelJobRequest.SerializeToString,
            yandex_dot_cloud_dot_operation_dot_operation__pb2.Operation.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
