from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from dice import Dice


class RewardID(Enum):
    ITEM = auto()
    GOLD_AND_TRINKET = auto()


@dataclass
class RewardInfo:
    reward_id: RewardID
    name: str
    award_item: bool = False
    award_trinket: bool = False
    award_gold: bool = False
    gold_dice: Dice = None

    @staticmethod
    def from_id(reward_id: RewardID):
        return _REWARDS[reward_id]


_REWARDS = {
    RewardID.ITEM: RewardInfo(reward_id=RewardID.ITEM, name="Item", award_item=True),
    RewardID.GOLD_AND_TRINKET: RewardInfo(
        reward_id=RewardID.GOLD_AND_TRINKET,
        name="Gold and a Trinket",
        award_trinket=True,
        award_gold=True,
        gold_dice=Dice(number=2, sides=20, modifier=60),
    ),
}
