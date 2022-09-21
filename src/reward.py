from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto

from helpers import Dice


class RewardId(Enum):
    ITEM = auto()
    GOLD_AND_TRINKET = auto()


@dataclass
class Reward:
    reward_id: RewardId
    gold_dice: Dice = None
