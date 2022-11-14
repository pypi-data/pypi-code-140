from __future__ import annotations

import os
import time
import types
from typing import Any, Dict, List, TYPE_CHECKING, Type, Tuple

import ulid

from ..serialize import get_callsite_data


if TYPE_CHECKING:
    # Literal and TypedDict only exist on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import Literal, TypedDict
    from ..serialize import UserCodeCallSite
    from django.db.models.sql.compiler import SQLUpdateCompiler

    class QueryStart(TypedDict):
        frame_id: str
        user_code_call_site: UserCodeCallSite | None
        call_timestamp: float
        timestamp: float
        type: Literal["start_sql_query"]

    class QueryEnd(TypedDict, total=False):
        frame_id: str
        query: str | None
        query_data: List[Any] | str | None
        query_template: str | None
        return_timestamp: float
        timestamp: float
        type: Literal["end_sql_query"]


class SQLQueryFilter:
    co_names: Tuple[str, ...] = ("execute_sql",)
    django_sql_filename = os.path.normpath("/django/db/models/sql/compiler.py")
    klass: Type[SQLUpdateCompiler] | None = None

    def __init__(self, config) -> None:
        self.config = config
        self._frame_ids: Dict[int, str] = {}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        if (
            self.django_sql_filename in frame.f_code.co_filename
            and frame.f_code.co_name in self.co_names
        ):  # pragma: no cover
            # Doing the import once and binding is substantially faster than going
            # through the import system every time.
            # See:
            # https://github.com/django/asgiref/issues/269
            # https://github.com/django/asgiref/pull/288
            # A more battle-tested (slightly slower/more complex) alternative would be:
            # https://github.com/django/django/pull/14850
            # https://github.com/django/django/pull/14858
            # https://github.com/django/django/pull/14931
            if SQLQueryFilter.klass is None:
                from django.db.models.sql.compiler import SQLUpdateCompiler

                SQLQueryFilter.klass = SQLUpdateCompiler
            return frame.f_code is not SQLQueryFilter.klass.execute_sql.__code__
        return False

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: Any,
        call_frame_ids: List[Dict[str, str]],
    ):
        timestamp = time.time()
        if event == "call":
            frame_id = f"frm_{ulid.new()}"
            self._frame_ids[id(frame)] = frame_id
            if call_frame_ids:
                user_code_call_site = get_callsite_data(frame, call_frame_ids[-1])
            else:
                user_code_call_site = None

            query_start: QueryStart = {
                "frame_id": frame_id,
                "user_code_call_site": user_code_call_site,
                "call_timestamp": time.time(),
                "timestamp": timestamp,
                "type": "start_sql_query",
            }
            return query_start

        assert event == "return"

        try:
            sql = frame.f_locals["sql"]
            params = frame.f_locals["params"]
        except KeyError:
            query_template = None
            query = None
        else:
            if sql == "":
                query_template = None
                query = None
            else:
                cursor = frame.f_locals["cursor"]
                ops = frame.f_locals["self"].connection.ops
                query_template = sql.strip()
                query = ops.last_executed_query(cursor, sql, params).strip()

        query_end: QueryEnd = {
            "frame_id": self._frame_ids[id(frame)],
            "return_timestamp": timestamp,
            "query_template": query_template,
            "query": query,
            "query_data": arg,
            "timestamp": timestamp,
            "type": "end_sql_query",
        }
        return query_end
