"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Callable,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)


DEFINITION = """
query ChangeTypes($name: String) {
  change_types: change_types_v1(name: $name) {
    name
    priority
    contextType
    contextSchema
    disabled
    changes {
      provider
      changeSchema
      context {
        selector
        when
      }
      ... on ChangeTypeChangeDetectorJsonPathProvider_v1 {
        jsonPathSelectors
      }
    }
    inherit {
      name
    }
  }
}
"""


class ChangeTypeChangeDetectorContextSelectorV1(BaseModel):
    selector: str = Field(..., alias="selector")
    when: Optional[str] = Field(..., alias="when")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ChangeTypeChangeDetectorV1(BaseModel):
    provider: str = Field(..., alias="provider")
    change_schema: Optional[str] = Field(..., alias="changeSchema")
    context: Optional[ChangeTypeChangeDetectorContextSelectorV1] = Field(
        ..., alias="context"
    )

    class Config:
        smart_union = True
        extra = Extra.forbid


class ChangeTypeChangeDetectorJsonPathProviderV1(ChangeTypeChangeDetectorV1):
    json_path_selectors: list[str] = Field(..., alias="jsonPathSelectors")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ChangeTypeV1_ChangeTypeV1(BaseModel):
    name: str = Field(..., alias="name")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ChangeTypeV1(BaseModel):
    name: str = Field(..., alias="name")
    priority: str = Field(..., alias="priority")
    context_type: str = Field(..., alias="contextType")
    context_schema: Optional[str] = Field(..., alias="contextSchema")
    disabled: Optional[bool] = Field(..., alias="disabled")
    changes: list[
        Union[ChangeTypeChangeDetectorJsonPathProviderV1, ChangeTypeChangeDetectorV1]
    ] = Field(..., alias="changes")
    inherit: Optional[list[ChangeTypeV1_ChangeTypeV1]] = Field(..., alias="inherit")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ChangeTypesQueryData(BaseModel):
    change_types: Optional[list[ChangeTypeV1]] = Field(..., alias="change_types")

    class Config:
        smart_union = True
        extra = Extra.forbid


def query(query_func: Callable, **kwargs) -> ChangeTypesQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        ChangeTypesQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return ChangeTypesQueryData(**raw_data)
