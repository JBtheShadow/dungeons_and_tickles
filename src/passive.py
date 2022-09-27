from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class PassiveID(Enum):
    AUTO_GROW_AT = auto()


class PassiveType(Enum):
    PERSISTENT = auto()


@dataclass
class PassiveInfo:
    """
    Seeing as items, status effects, abilities or even classes may have
    varying effects that need to be managed in between actions, turns or
    battles, this is a tentative effort to combine it all into one place.

    Nothing much here at the moment, I'll need to think it up a little more.
    """

    passive_id: PassiveID
    name: str
    description: str
    passive_type: PassiveType

    @staticmethod
    def from_id(passive_id: PassiveID):
        return _PASSIVES.get(passive_id)


_PASSIVES = {
    PassiveID.AUTO_GROW_AT: PassiveInfo(
        passive_id=PassiveID.AUTO_GROW_AT,
        name="Auto Grow AT",
        description="Increases AT by 1 every round after the first",
        passive_type=PassiveType.PERSISTENT,
    ),
}
