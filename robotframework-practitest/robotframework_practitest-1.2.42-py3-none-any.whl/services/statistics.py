from __future__ import annotations

import time
from enum import Enum
from time import sleep
from typing import List

import pandas

from robotframework_practitest.utils import get_error_info
from robotframework_practitest.utils.logger import LOGGER as logger

DEFAULT_RETENTION_TIMEOUT = 300
PENDING_RETENTION_TIMEOUT = 60


class _Color(Enum):
    FAILED = 'red'
    PASSED = 'green'
    SKIPPED = 'yellow'
    Default = 'grey'


class TestStates(Enum):
    Robot = 'robot'
    PractiTest = 'practi_test'
    Status = 'status'
    Path = 'path'

    @staticmethod
    def as_tuple():
        return TestStates.Robot, TestStates.PractiTest, TestStates.Status


class TestStatuses(Enum):
    NotRun = 'not_run'
    Pending = 'Pending'
    PASSED = 'passed'
    FAILED = 'failed'
    SKIPPED = 'skipped'


class RowItem(dict):
    def __init__(self, **kwargs):
        for col in TestStates:
            self[col.name] = kwargs.get(col.name, None)

    def __str__(self):
        return ', '.join([f"{col.name}={getattr(self, col.name)}" for col in TestStates])

    def __eq__(self, other):
        try:
            assert isinstance(other, type(self))
            assert other[TestStates.Robot.name] == self[TestStates.Robot.name]
            assert other[TestStates.Path.name] == self[TestStates.Path.name]
        except AssertionError:
            return False
        else:
            return True


class _TestTable(list, List[RowItem]):
    def set_tests(self, col: TestStates, *tests, status: TestStatuses = None, path=None, update=None):
        if path is None:
            path = []
        if col == TestStates.Robot:
            for test in tests:
                row_item = RowItem(**{TestStates.Robot.name: test, TestStates.PractiTest.name: '-',
                                      TestStates.Status.name: TestStatuses.NotRun.name, TestStates.Path.name: path})
                self.append(row_item)
        elif col == TestStates.PractiTest:
            for test in tests:
                for i, item in enumerate(self):
                    current_item = RowItem(**{TestStates.Robot.name: test, TestStates.Path.name: path})
                    if current_item == self[i]:
                        self[i][TestStates.PractiTest.name] = update
                        if status:
                            self[i][TestStates.Status.name] = status.name
                        break
        elif col == TestStates.Status:
            assert status, f"State {col.name} require status"
            for test in tests:
                for i, item in enumerate(self):
                    current_item = RowItem(**{TestStates.Robot.name: test, TestStates.Path.name: path})
                    if current_item == self[i]:
                        self[i][TestStates.Status.name] = status.name
                        break

    def as_dict(self, *columns, **filters):
        columns = columns if len(columns) > 0 else TestStates.as_tuple()
        res_dict = {col.name: [] for col in columns}
        for row in self:
            if len(filters) > 0:
                for field, value in filters.items():
                    if isinstance(value, (list, tuple)):
                        if row.get(field) not in (v.name for v in value):
                            continue
                    else:
                        if row.get(field) != value.name:
                            continue
                    for col in columns:
                        res_dict[col.name].append(row.get(col.name))
            else:
                for col in columns:
                    res_dict[col.name].append(row.get(col.name))
        return res_dict

    def df(self, *columns, **filters):
        return pandas.DataFrame.from_dict(self.as_dict(*columns, **filters))

    @staticmethod
    def _field_formatter(value):
        return value

    @staticmethod
    def _status_formatter(value):
        try:
            color = _Color[value]
        except Exception as e:
            color = _Color.Default

        return f"<font color='{color.value}'>{value}</font>"

    def show(self, *columns, html=False, **filters):
        df = self.df(*columns, **filters)
        pandas.set_option("display.precision", 2)
        pandas.set_option('display.max_rows', None)
        pandas.set_option('display.max_columns', None)
        pandas.set_option("max_colwidth", 500)
        pandas.set_option('display.colheader_justify', 'left')
        pandas.set_option('display.width', 10000)
        return df.to_html(justify='center') if html else df.to_string(justify='center')

    def wait_state(self, timeout=DEFAULT_RETENTION_TIMEOUT):
        logger.console(f"{self}; Waiting to complete all tests")
        statuses = {TestStates.Status.name: (TestStatuses.NotRun, TestStatuses.Pending)}
        start_ts = time.perf_counter()
        display_ts = time.perf_counter()
        while True:
            try:
                assert len(self.as_dict(TestStates.PractiTest, **statuses).get(TestStates.PractiTest.name)) > 0
                if (time.perf_counter() - start_ts) >= timeout:
                    raise TimeoutError("Test completion taking too much time")
                if (time.perf_counter() - display_ts) >= PENDING_RETENTION_TIMEOUT:
                    logger.console(f"\nPractiTest reporter: Tests not completed yet:\n{self.show(TestStates.Robot, TestStates.Status, **statuses)}")
                    display_ts = time.perf_counter()
                sleep(1)
            except AssertionError:
                logger.console(f"All tests completed:\nTest list:\n{self.show()}")
                break
            except TimeoutError as e:
                logger.error(f"PractiTest reporter: {e}\nTests not completed yet:\n\n{self.show()}\n")
                raise
            except Exception as e:
                f, li = get_error_info()
                logger.error(f"{type(e).__name__}: {e}; File: {f}:{li}")
                raise


DataStatistics = _TestTable


__all__ = [
    'TestStates',
    'TestStatuses',
    'DataStatistics'
]
