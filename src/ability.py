from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class StatID(Enum):
    AT = auto()


class StatusID(Enum):
    LGI = auto()  # Laughing Gas Intoxication
    TS = auto()  # Ticklish Sensations
    REGEN = auto()
    LRA = auto()  # Laugh Resist Aura
    EVADE = auto()
    BLIND = auto()
    WEAKEN = auto()
    STRENGTHEN = auto()


class AbilityID(Enum):

    # Item Abilities
    ESCAPE_FROM_BATTLE = auto()
    MINES_MODIFIER = auto()
    ANY_ROLL_MODIFIER = auto()
    UNSTACKABLE_BATTLE_MODIFIER = auto()
    CHOOSE_ONE = auto()
    FORCE_MOVE_TO_LOCATION = auto()
    LEARN_NEW_SPELL = auto()
    UNSTACKABLE_MISC_MODIFIER = auto()

    # Enemy Abilities
    ALL_DAMAGE_TAKEN_SET_TO_1 = auto()
    DAMAGE_EVERY_X_TURNS = auto()
    FAINT_IN_X_TURNS = auto()
    IMMUNE_EVERY_X_TURNS = auto()
    FIXED_DAMAGE_EVERY_X_HITS = auto()
    HEAL_ST_EVERY_X_HITS = auto()
    CAST_SPELL_EVERY_X_TURNS = auto()
    FIXED_DAMAGE_ON_PLAYER_MISS = auto()
    HEAL_EP_EVERY_X_TURNS = auto()
    DAMAGE_AFTER_X_TURNS_ON_HIT = auto()
    CHANCE_TO_EVADE = auto()
    INFLICT_STATUS_ON_HIT = auto()


@dataclass
class Ability:
    ability_id: AbilityID
    dmg_dice: tuple = None
    status_id: StatusID = None
    chance_dice: tuple = None
    turns: int = None
    dmg: int = None
    heal: int = None
    hits: int = None
    target: int = None
    level: int = None
