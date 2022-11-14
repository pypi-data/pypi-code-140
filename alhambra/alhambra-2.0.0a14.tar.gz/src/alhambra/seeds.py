from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING, Any, Callable, Sequence, Type, TypeVar, cast

import attrs

import scadnano

if TYPE_CHECKING:
    from alhambra.tilesets import XgrowGlueOpts
    import xgrow.tileset as xgt

from .glues import DXGlue, Glue, glue_factory

T = TypeVar("T")


class Seed(ABC):
    """Abstact Base Class for a seed structure.

    Generally, seeds need:

    - A method to convert the seed to xgrow-usable information.
    - Methods to convert the seed to and from a dict, for storage
    """

    @abstractmethod
    def to_xgrow(
        self,
        gluenamemap: Callable[[str], str] = lambda x: x,
        offset: tuple[int, int] = (0, 0),
    ) -> tuple[list[xgt.Tile], list[xgt.Bond], xgt.InitState]:
        """Create xgrow implementation of the seed.

        Converts the Seed to a list of xgrow tiles to add to a system, a list of bonds to add,
        and an initial state.
        """
        raise NotImplementedError

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_dict(cls: Type[T], d: dict) -> T:
        raise NotImplementedError


class SeedSupportingScadnano(Seed):
    @abstractmethod
    def ho_from_seed_offset(
        self, seed_offset: tuple[int, int], gridysize: int
    ) -> tuple[int, int]:
        ...

    @abstractmethod
    def to_scadnano(
        self, design: scadnano.Design, helix: int, offset: int
    ) -> list[scadnano.Strand]:
        ...


class SeedFactory:
    types: dict[str, Type[Seed]]

    def __init__(self):
        self.types = {}

    def register(self, c: Type[Seed], n: Optional[str] = None):
        self.types[n if n is not None else c.__name__] = c

    def from_dict(self, d: dict[str, Any]) -> Seed:
        if "type" in d:
            c = self.types[d["type"]]
            return c.from_dict({k: v for k, v in d.items() if k != "type"})
        else:
            raise ValueError


class DXOrigamiSeed(Seed):
    ...


def _convert_adapts(
    adapters: Sequence[tuple[str | Glue, str | Glue]]
) -> list[tuple[Glue, Glue]]:
    # todo: verify
    return [
        (
            Glue(a[0]) if not isinstance(a[0], Glue) else a[0],
            Glue(a[1]) if not isinstance(a[1], Glue) else a[1],
        )
        for a in adapters
    ]


@attrs.define()
class DiagonalSESeed(Seed):
    "Tall rectangle origami to DX-tile seed (Barish et al)"
    # FIXME: fixed-choice adapters for now
    adapters: Sequence[tuple[Glue, Glue]] = attrs.field(
        converter=_convert_adapts, on_setattr=attrs.setters.convert
    )

    def to_dict(self) -> dict:
        d: dict[str, Any] = {}
        d["type"] = self.__class__.__name__
        d["adapters"] = [(g1.to_dict(), g2.to_dict()) for g1, g2 in self.adapters]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DiagonalSESeed:
        d["adapters"] = [
            (glue_factory.from_dict(g1), glue_factory.from_dict(g2))
            for g1, g2 in d["adapters"]
        ]
        return cls(**d)

    def to_xgrow(
        self,
        gluenamemap: Callable[[str], str] = lambda x: x,
        offset: tuple[int, int] = (0, 0),
    ) -> tuple[list[xgt.Tile], list[xgt.Bond], xgt.InitState]:
        import xgrow.tileset as xgt

        xgtiles = []
        locs: list[tuple[int, int, str]] = []
        bonds = [xgt.Bond("seed", 100)]

        xgtiles.append(
            xgt.Tile([0, "seed", "seed", "seed"], "seed", stoic=0, color="white")
        )

        y = len(self.adapters) + offset[1]  # + 1
        x = 1 + offset[0]
        for i, (eg, sg) in enumerate(self.adapters):
            egn, sgn = gluenamemap(eg.ident()), gluenamemap(sg.ident())
            xa = xgt.Tile(
                ["seed", egn, sgn, "seed"],
                f"adapter_{i}",
                stoic=0,
                color="brown",
            )
            locs.append((x, y, cast(str, xa.name)))
            if x != 1:
                locs.append((x - 1, y, "seed"))
            x += 1
            y -= 1
            xgtiles.append(xa)

        return xgtiles, bonds, xgt.InitState(locs)


seed_factory = SeedFactory()

seed_factory.register(DiagonalSESeed, "longrect")
# seed_factory.register(DX_TallRect, "tallrect")
# seed_factory.register(DX_TallRect)
