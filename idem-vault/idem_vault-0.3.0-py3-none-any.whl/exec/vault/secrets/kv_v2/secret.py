from typing import Dict

import dict_tools.data


async def get(hub, ctx, path: str, version: int = None) -> Dict:
    """
    KV_v2 secret data-source.

    Args:
        path(string): The full logical path to write the data. This should be prefixed 'with secret/'.
        version(int, optional): The version of the secret to read. If not specified, the latest version will be used.

    Request Syntax:
        [Idem-state-name]:
          exec.run:
            - path: vault.secrets.kv_v2.secret.get
            - kwargs:
                path: 'string'
                version: int

    Examples:
        my-secret:
          exec.run:
            - path: vault.secrets.kv_v2.secret.get
            - kwargs:
                path: secret/test
                version: 1

    """
    result = dict(comment=[], ret=None, result=True)
    read_ret = await hub.exec.hvac.client.secrets.kv.v2.read_secret_version(
        ctx=ctx, path=path, version=version
    )
    if not read_ret["result"]:
        result["result"] = False
        result["comment"] += list(read_ret["comment"])
        return result

    result["ret"] = {
        "path": path,
        "data": dict_tools.data.SafeNamespaceDict(read_ret["ret"]["data"]["data"]),
    }
    return result
