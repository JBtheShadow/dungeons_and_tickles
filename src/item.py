from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class TrinketId(Enum):
    GRINDSTONE = auto()
    RING_ENDURANCE = auto()
    GOLDEN_FEATHER = auto()
    BROKEN_FEATHERARROW = auto()
    LIQUID_LAUGHTER_VIAL = auto()
    SWIFT_FEATHER = auto()


@dataclass
class Trinket:
    name: str


TRINKETS = {
    TrinketId.GRINDSTONE:
        Trinket('Grindstone'),
    TrinketId.RING_ENDURANCE:
        Trinket('Ring of Endurance'),
    TrinketId.GOLDEN_FEATHER:
        Trinket('Golden Feather'),
    TrinketId.BROKEN_FEATHERARROW:
        Trinket('Broken Featherarrow'),
    TrinketId.LIQUID_LAUGHTER_VIAL:
        Trinket('Liquid Laughter Vial'),
    TrinketId.SWIFT_FEATHER:
        Trinket('Swift Feather'),
}
