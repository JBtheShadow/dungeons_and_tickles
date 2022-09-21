from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class TrapType(Enum):
    DIRECT_DAMAGE = auto()


@dataclass
class Trap:
    name: str
    trap_type: TrapType
    dmg: int = None
