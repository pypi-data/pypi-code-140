import socket
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ContextManager, Iterator, List, Tuple, Union, cast

import grpc

from isolate.backends import (
    BasicCallable,
    CallResultType,
    EnvironmentConnection,
)
from isolate.connections._local import PythonExecutionBase, agent_startup
from isolate.connections.common import serialize_object
from isolate.connections.grpc import agent, definitions
from isolate.connections.grpc.interface import from_grpc, to_grpc
from isolate.logs import Log, LogLevel, LogSource


class AgentError(Exception):
    """An internal problem caused by (most probably) the agent."""


@dataclass
class GRPCExecutionBase(EnvironmentConnection):
    """A customizable gRPC-based execution backend."""

    def start_agent(self) -> ContextManager[Tuple[str, grpc.ChannelCredentials]]:
        """Starts the gRPC agent and returns the address it is listening on and
        the required credentials to connect to it."""
        raise NotImplementedError

    def _run_through_grpc(
        self,
        function: definitions.SerializedObject,
        *,
        max_wait_timeout: float = 10,
    ) -> Iterator[definitions.PartialRunResult]:
        """Starts a new agent process, sends the given 'function' to the agent and
        awaits until the result is received. This function takes and returns raw gRPC
        messages (use `run()` to actually execute Python functions and receive Python
        objects).

        If the gRPC server is not accessible at the passed maximum timeout, an
        AgentError will be raised."""

        # Implementation details
        # ======================
        #
        #  RPC Flow:
        #  ---------
        #  1. [controller]: Spawn the agent.
        #  2.      [agent]: Start listening at the given address.
        #  3. [controller]: Await *at most* max_wait_timeout seconds for the agent to be available
        #                   if it doesn't do it until then, raise an AgentError.
        #  4. [controller]: If the server is available, then establish the bridge and pass the
        #                   'function' as the input.
        #  5.      [agent]: Receive the function, deserialize it, start the execution.
        #  6. [controller]: Watch agent for logs (stdout/stderr), and as soon as they appear
        #                   call the log handler.
        #  7.      [agent]: Once the execution of the function is finished, send the result
        #                   using the same serialization method.
        #  8. [controller]: Receive the result back and return it.

        with self.start_agent() as (address, credentials):
            with grpc.secure_channel(address, credentials) as channel:
                channel_status = grpc.channel_ready_future(channel)
                try:
                    channel_status.result(timeout=max_wait_timeout)
                except grpc.FutureTimeoutError:
                    raise AgentError(
                        f"Couldn't connect to the gRPC server in the agent (listening at {address}) "
                        "in time."
                    )

                agent = definitions.AgentStub(channel)
                yield from agent.Run(function)

    def run(
        self,
        executable: BasicCallable,
        *args: Any,
        **kwargs: Any,
    ) -> CallResultType:
        method = self.environment.settings.serialization_method
        function = definitions.SerializedObject(
            method=method,
            definition=serialize_object(method, executable),
            was_it_raised=False,
        )

        for partial_result in self._run_through_grpc(function):
            for raw_log in partial_result.logs:
                log = from_grpc(raw_log)
                self.log(log.message, level=log.level, source=log.source)

            if partial_result.is_complete:
                if not partial_result.result:
                    raise AgentError(
                        "The agent didn't return a result, but it should have."
                    )

                return cast(CallResultType, from_grpc(partial_result.result))

        raise AgentError(
            "No result object was received from the agent (it never set is_complete to True)."
        )


class LocalPythonGRPC(PythonExecutionBase[str], GRPCExecutionBase):
    @contextmanager
    def start_agent(self) -> Iterator[Tuple[str, grpc.ChannelCredentials]]:
        def find_free_port() -> Tuple[str, int]:
            """Find a free port in the system."""
            with socket.socket() as _temp_socket:
                _temp_socket.bind(("", 0))
                return _temp_socket.getsockname()

        host, port = find_free_port()
        address = f"{host}:{port}"
        process = None
        try:
            with self.start_process(address) as process:
                yield address, grpc.local_channel_credentials()
        finally:
            if process is not None:
                # TODO: should we check the status code here?
                process.terminate()

    def get_python_cmd(
        self,
        executable: Path,
        connection: str,
    ) -> List[Union[str, Path]]:
        return [
            executable,
            agent_startup.__file__,
            agent.__file__,
            connection,
        ]

    def handle_agent_log(self, line: str, level: LogLevel) -> None:
        self.log(line, level=level, source=LogSource.USER)
