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

from reconcile.gql_definitions.vpc_peerings_validator.vpc_peerings_validator_peered_cluster_fragment import (
    VpcPeeringsValidatorPeeredCluster,
)


DEFINITION = """
fragment VpcPeeringsValidatorPeeredCluster on Cluster_v1 {
  name
  spec {
    private
  }
  internal
}

query VpcPeeringsValidator {
  clusters: clusters_v1 {
    name
    spec {
      private
    }
    internal
    peering {
      connections {
        provider
        ... on ClusterPeeringConnectionClusterRequester_v1 {
          cluster {
            ... VpcPeeringsValidatorPeeredCluster
          }
        }
        ... on ClusterPeeringConnectionClusterAccepter_v1 {
          cluster {
            ... VpcPeeringsValidatorPeeredCluster
          }
        }
      }
    }
  }
}
"""


class ClusterSpecV1(BaseModel):
    private: bool = Field(..., alias="private")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ClusterPeeringConnectionV1(BaseModel):
    provider: str = Field(..., alias="provider")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ClusterPeeringConnectionClusterRequesterV1(ClusterPeeringConnectionV1):
    cluster: VpcPeeringsValidatorPeeredCluster = Field(..., alias="cluster")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ClusterPeeringConnectionClusterAccepterV1(ClusterPeeringConnectionV1):
    cluster: VpcPeeringsValidatorPeeredCluster = Field(..., alias="cluster")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ClusterPeeringV1(BaseModel):
    connections: list[
        Union[
            ClusterPeeringConnectionClusterRequesterV1,
            ClusterPeeringConnectionClusterAccepterV1,
            ClusterPeeringConnectionV1,
        ]
    ] = Field(..., alias="connections")

    class Config:
        smart_union = True
        extra = Extra.forbid


class ClusterV1(BaseModel):
    name: str = Field(..., alias="name")
    spec: Optional[ClusterSpecV1] = Field(..., alias="spec")
    internal: Optional[bool] = Field(..., alias="internal")
    peering: Optional[ClusterPeeringV1] = Field(..., alias="peering")

    class Config:
        smart_union = True
        extra = Extra.forbid


class VpcPeeringsValidatorQueryData(BaseModel):
    clusters: Optional[list[ClusterV1]] = Field(..., alias="clusters")

    class Config:
        smart_union = True
        extra = Extra.forbid


def query(query_func: Callable, **kwargs) -> VpcPeeringsValidatorQueryData:
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
        VpcPeeringsValidatorQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return VpcPeeringsValidatorQueryData(**raw_data)
