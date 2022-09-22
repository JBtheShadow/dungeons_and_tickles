from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class RewardID(Enum):
    ITEM = auto()
    GOLD_AND_TRINKET = auto()


@dataclass
class Reward:
    reward_id: RewardID
    gold_dice: tuple = None
