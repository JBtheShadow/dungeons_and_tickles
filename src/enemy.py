from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from secrets import choice

from helpers import Dice
from status import StatusId
from trinket import TrinketId


class ModifierId(Enum):
    UNNATURALLY_TICKLISH = auto()
    TOUGH = auto()
    BIG = auto()
    MISCHIEVOUS = auto()
    BLESSED_BY_LAUGHTER = auto()
    CURSED = auto()


class EnemyAbilityId(Enum):
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
class EnemyAbility:
    ability_id: EnemyAbilityId
    dmg_dice: Dice = None
    status_id: StatusId = None
    chance_dice: Dice = None
    turns: int = None
    dmg: int = None
    heal: int = None
    hits: int = None
    target: int = None
    level: int = None


@dataclass
class Enemy:
    name: str
    max_st: int = None
    max_ep: int = 0
    dmg: int = None
    modifier_id: ModifierId = None
    trinket_id: TrinketId = None
    abilities: list[EnemyAbility] = None
    level: int = 0
    gold: int = 50

    st: int = field(init=False)
    ep: int = field(init=False)

    def __post_init__(self):
        self.abilities = self.abilities or []
        one_dmg = EnemyAbilityId.ALL_DAMAGE_TAKEN_SET_TO_1 in self.abilities

        # Level
        if self.level:
            self.max_st += (10 if not one_dmg else 1) * self.level
            self.dmg += 10 * self.level

            faint_abilities = [
                x for x in self.abilities
                if x.ability_id == EnemyAbilityId.FAINT_IN_X_TURNS
            ]
            if faint_abilities:
                faint_abilities[0].turns += self.level

        # Modifier
        if not self.modifier_id and self.level:
            self.modifier_id = choice(list(ModifierId))

        if self.modifier_id == ModifierId.UNNATURALLY_TICKLISH:
            self.name = 'Unnaturally Ticklish ' + self.name
            self.max_st -= 5 if not one_dmg else 1
        if self.modifier_id == ModifierId.TOUGH:
            self.name = 'Tough ' + self.name
            self.max_ep += 2
        if self.modifier_id == ModifierId.BIG:
            if 'Big' in self.name:
                self.name = self.name.replace('Big', 'Gargantuan')
            elif 'Small' in self.name:
                self.name = self.name.replace('Small', 'Not So Small')
            else:
                self.name = 'Big ' + self.name
            self.max_st += 20 if not one_dmg else 2
            self.max_ep += 1
        if self.modifier_id == ModifierId.MISCHIEVOUS:
            self.name = 'Mischievous ' + self.name
            self.dmg += 10
        if self.modifier_id == ModifierId.BLESSED_BY_LAUGHTER:
            self.name = 'Blessed ' + self.name
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.HEAL_ST_EVERY_X_HITS,
                heal=(5 if not one_dmg else 1),
                hits=(1 if not one_dmg else 2)))
        if self.modifier_id == ModifierId.CURSED:
            self.name = 'Cursed ' + self.name
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.CAST_SPELL_EVERY_X_TURNS,
                turns=2))

        # Trinkets
        if not self.trinket_id and self.level and self.level % 3 == 0:
            self.trinket_id = choice(list(TrinketId))

        if self.trinket_id == TrinketId.GRINDSTONE:
            self.dmg += 2
        if self.trinket_id == TrinketId.RING_ENDURANCE:
            if self.max_ep <= 0:
                self.max_ep = 1
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.HEAL_EP_EVERY_X_TURNS,
                heal=1, turns=5))
        if self.trinket_id == TrinketId.GOLDEN_FEATHER:
            self.gold += 10
        if self.trinket_id == TrinketId.BROKEN_FEATHERARROW:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.DAMAGE_AFTER_X_TURNS_ON_HIT,
                Dice(1, 20), turns=5))
        if self.trinket_id == TrinketId.LIQUID_LAUGHTER_VIAL:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.INFLICT_STATUS_ON_HIT,
                status_id=StatusId.LGI, level=1))
        if self.trinket_id == TrinketId.SWIFT_FEATHER:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.CHANCE_TO_EVADE,
                chance_dice=Dice(1, 10), target=10))

        # Final stats
        self.st = self.max_st
        self.ep = self.max_ep
