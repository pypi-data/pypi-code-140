# coding=utf-8
# Copyright 2022-present, the HuggingFace Inc. team.
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
"""Contains utilities to handle headers to send in calls to Huggingface Hub."""
from typing import Dict, Optional, Union

from ..constants import HF_HUB_DISABLE_IMPLICIT_TOKEN
from ._hf_folder import HfFolder
from ._runtime import (
    get_fastai_version,
    get_fastcore_version,
    get_hf_hub_version,
    get_python_version,
    get_tf_version,
    get_torch_version,
    is_fastai_available,
    is_fastcore_available,
    is_tf_available,
    is_torch_available,
)
from ._validators import validate_hf_hub_args


@validate_hf_hub_args
def build_hf_headers(
    *,
    token: Optional[Union[bool, str]] = None,
    is_write_action: bool = False,
    library_name: Optional[str] = None,
    library_version: Optional[str] = None,
    user_agent: Union[Dict, str, None] = None,
) -> Dict[str, str]:
    """
    Build headers dictionary to send in a HF Hub call.

    By default, authorization token is always provided either from argument (explicit
    use) or retrieved from the cache (implicit use). To explicitly avoid sending the
    token to the Hub, set `token=False` or set the `HF_HUB_DISABLE_IMPLICIT_TOKEN`
    environment variable.

    In case of an API call that requires write access, an error is thrown if token is
    `None` or token is an organization token (starting with `"api_org***"`).

    In addition to the auth header, a user-agent is added to provide information about
    the installed packages (versions of python, huggingface_hub, torch, tensorflow,
    fastai and fastcore).

    Args:
        token (`str`, `bool`, *optional*):
            The token to be sent in authorization header for the Hub call:
                - if a string, it is used as the Hugging Face token
                - if `True`, the token is read from the machine (cache or env variable)
                - if `False`, authorization header is not set
                - if `None`, the token is read from the machine only except if
                  `HF_HUB_DISABLE_IMPLICIT_TOKEN` env variable is set.
        is_write_action (`bool`, default to `False`):
            Set to True if the API call requires a write access. If `True`, the token
            will be validated (cannot be `None`, cannot start by `"api_org***"`).
        library_name (`str`, *optional*):
            The name of the library that is making the HTTP request. Will be added to
            the user-agent header.
        library_version (`str`, *optional*):
            The version of the library that is making the HTTP request. Will be added
            to the user-agent header.
        user_agent (`str`, `dict`, *optional*):
            The user agent info in the form of a dictionary or a single string. It will
            be completed with information about the installed packages.

    Returns:
        A `Dict` of headers to pass in your API call.

    Example:
    ```py
        >>> build_hf_headers(token="hf_***") # explicit token
        {"authorization": "Bearer hf_***", "user-agent": ""}

        >>> build_hf_headers(token=True) # explicitly use cached token
        {"authorization": "Bearer hf_***",...}

        >>> build_hf_headers(token=False) # explicitly don't use cached token
        {"user-agent": ...}

        >>> build_hf_headers() # implicit use of the cached token
        {"authorization": "Bearer hf_***",...}

        # HF_HUB_DISABLE_IMPLICIT_TOKEN=True # to set as env variable
        >>> build_hf_headers() # token is not sent
        {"user-agent": ...}

        >>> build_hf_headers(token="api_org_***", is_write_action=True)
        ValueError: You must use your personal account token for write-access methods.

        >>> build_hf_headers(library_name="transformers", library_version="1.2.3")
        {"authorization": ..., "user-agent": "transformers/1.2.3; hf_hub/0.10.2; python/3.10.4; tensorflow/1.55"}
    ```

    Raises:
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If organization token is passed and "write" access is required.
        [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)
            If "write" access is required but token is not passed and not saved locally.
        [`EnvironmentError`](https://docs.python.org/3/library/exceptions.html#EnvironmentError)
            If `token=True` but token is not saved locally.
    """
    # Get auth token to send
    token_to_send = get_token_to_send(token)
    _validate_token_to_send(token_to_send, is_write_action=is_write_action)

    # Combine headers
    headers = {
        "user-agent": _http_user_agent(
            library_name=library_name,
            library_version=library_version,
            user_agent=user_agent,
        )
    }
    if token_to_send is not None:
        headers["authorization"] = f"Bearer {token_to_send}"
    return headers


def get_token_to_send(token: Optional[Union[bool, str]]) -> Optional[str]:
    """Select the token to send from either `token` or the cache."""
    # Case token is explicitly provided
    if isinstance(token, str):
        return token

    # Case token is explicitly forbidden
    if token is False:
        return None

    # Token is not provided: we get it from local cache
    cached_token = HfFolder().get_token()

    # Case token is explicitly required
    if token is True:
        if cached_token is None:
            raise EnvironmentError(
                "Token is required (`token=True`), but no token found. You"
                " need to provide a token or be logged in to Hugging Face with"
                " `huggingface-cli login` or `huggingface_hub.login`. See"
                " https://huggingface.co/settings/tokens."
            )
        return cached_token

    # Case implicit use of the token is forbidden by env variable
    if HF_HUB_DISABLE_IMPLICIT_TOKEN:
        return None

    # Otherwise: we use the cached token as the user has not explicitly forbidden it
    return cached_token


def _validate_token_to_send(token: Optional[str], is_write_action: bool) -> None:
    if is_write_action:
        if token is None:
            raise ValueError(
                "Token is required (write-access action) but no token found. You need"
                " to provide a token or be logged in to Hugging Face with"
                " `huggingface-cli login` or `huggingface_hub.login`. See"
                " https://huggingface.co/settings/tokens."
            )
        if token.startswith("api_org"):
            raise ValueError(
                "You must use your personal account token for write-access methods. To"
                " generate a write-access token, go to"
                " https://huggingface.co/settings/tokens"
            )


def _http_user_agent(
    *,
    library_name: Optional[str] = None,
    library_version: Optional[str] = None,
    user_agent: Union[Dict, str, None] = None,
) -> str:
    """Format a user-agent string containing information about the installed packages.

    Args:
        library_name (`str`, *optional*):
            The name of the library that is making the HTTP request.
        library_version (`str`, *optional*):
            The version of the library that is making the HTTP request.
        user_agent (`str`, `dict`, *optional*):
            The user agent info in the form of a dictionary or a single string.

    Returns:
        The formatted user-agent string.
    """
    if library_name is not None:
        ua = f"{library_name}/{library_version}"
    else:
        ua = "unknown/None"
    ua += f"; hf_hub/{get_hf_hub_version()}"
    ua += f"; python/{get_python_version()}"
    if is_torch_available():
        ua += f"; torch/{get_torch_version()}"
    if is_tf_available():
        ua += f"; tensorflow/{get_tf_version()}"
    if is_fastai_available():
        ua += f"; fastai/{get_fastai_version()}"
    if is_fastcore_available():
        ua += f"; fastcore/{get_fastcore_version()}"
    if isinstance(user_agent, dict):
        ua += "; " + "; ".join(f"{k}/{v}" for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent
    return ua
