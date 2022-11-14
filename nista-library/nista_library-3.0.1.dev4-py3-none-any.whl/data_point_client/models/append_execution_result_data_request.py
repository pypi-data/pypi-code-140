from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.sub_series_request import SubSeriesRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="AppendExecutionResultDataRequest")


@attr.s(auto_attribs=True)
class AppendExecutionResultDataRequest:
    """
    Attributes:
        sub_series (List[SubSeriesRequest]):
        unit (Union[Unset, None, str]):
        execution_id (Union[Unset, str]):
    """

    sub_series: List[SubSeriesRequest]
    unit: Union[Unset, None, str] = UNSET
    execution_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sub_series = []
        for sub_series_item_data in self.sub_series:
            sub_series_item = sub_series_item_data.to_dict()

            sub_series.append(sub_series_item)

        unit = self.unit
        execution_id = self.execution_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "subSeries": sub_series,
            }
        )
        if unit is not UNSET:
            field_dict["unit"] = unit
        if execution_id is not UNSET:
            field_dict["executionId"] = execution_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        sub_series = []
        _sub_series = d.pop("subSeries")
        for sub_series_item_data in _sub_series:
            sub_series_item = SubSeriesRequest.from_dict(sub_series_item_data)

            sub_series.append(sub_series_item)

        unit = d.pop("unit", UNSET)

        execution_id = d.pop("executionId", UNSET)

        append_execution_result_data_request = cls(
            sub_series=sub_series,
            unit=unit,
            execution_id=execution_id,
        )

        return append_execution_result_data_request
