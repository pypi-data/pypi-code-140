from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.data_export_request import DataExportRequest
from ...models.problem_details import ProblemDetails
from ...types import Response


def _get_kwargs(
    workspace_id: str,
    file_id: str,
    *,
    client: Client,
    json_body: DataExportRequest,
) -> Dict[str, Any]:
    url = "{}/DataExport/workspace/{workspaceId}/file/{fileId}".format(
        client.base_url, workspaceId=workspace_id, fileId=file_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, ProblemDetails]]:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202
    if response.status_code == 400:
        response_400 = ProblemDetails.from_dict(response.json())

        return response_400
    if response.status_code == 401:
        response_401 = ProblemDetails.from_dict(response.json())

        return response_401
    if response.status_code == 403:
        response_403 = ProblemDetails.from_dict(response.json())

        return response_403
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, ProblemDetails]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace_id: str,
    file_id: str,
    *,
    client: Client,
    json_body: DataExportRequest,
) -> Response[Union[Any, ProblemDetails]]:
    """
    Args:
        workspace_id (str):
        file_id (str):
        json_body (DataExportRequest):

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        file_id=file_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace_id: str,
    file_id: str,
    *,
    client: Client,
    json_body: DataExportRequest,
) -> Optional[Union[Any, ProblemDetails]]:
    """
    Args:
        workspace_id (str):
        file_id (str):
        json_body (DataExportRequest):

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    return sync_detailed(
        workspace_id=workspace_id,
        file_id=file_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace_id: str,
    file_id: str,
    *,
    client: Client,
    json_body: DataExportRequest,
) -> Response[Union[Any, ProblemDetails]]:
    """
    Args:
        workspace_id (str):
        file_id (str):
        json_body (DataExportRequest):

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        file_id=file_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace_id: str,
    file_id: str,
    *,
    client: Client,
    json_body: DataExportRequest,
) -> Optional[Union[Any, ProblemDetails]]:
    """
    Args:
        workspace_id (str):
        file_id (str):
        json_body (DataExportRequest):

    Returns:
        Response[Union[Any, ProblemDetails]]
    """

    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            file_id=file_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
