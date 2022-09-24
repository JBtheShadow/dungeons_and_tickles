from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TrapID(Enum):
    # Encounter trap
    DIRECT_DAMAGE = auto()

    # Item traps
    TICKLE_TRAP = auto()
    TOLLBOOTH = auto()
    TICKLE_GLUE_TRAP = auto()
    TRIPWIRE = auto()


@dataclass
class Trap:
    name: str
    trap_id: TrapID
    dmg: int = 0
    mod: int = 0
    ends_turn: bool = False
