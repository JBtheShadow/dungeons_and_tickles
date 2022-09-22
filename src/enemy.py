from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from random import choice
from ability import Ability, AbilityID, StatusID
from item import TRINKETS, ItemID


class ModifierID(Enum):
    UNNATURALLY_TICKLISH = auto()
    TOUGH = auto()
    BIG = auto()
    MISCHIEVOUS = auto()
    BLESSED_BY_LAUGHTER = auto()
    CURSED = auto()


@dataclass
class Enemy:
    name: str
    max_st: int = None
    max_ep: int = 0
    dmg: int = None
    modifier_id: ModifierID = None
    trinket_id: ItemID = None
    abilities: list[Ability] = None
    level: int = 0
    gold: int = 50

    st: int = field(init=False)
    ep: int = field(init=False)

    def __post_init__(self):
        self.abilities = self.abilities or []
        one_dmg = AbilityID.ALL_DAMAGE_TAKEN_SET_TO_1 in self.abilities

        # Level
        if self.level:
            self.max_st += (10 if not one_dmg else 1) * self.level
            self.dmg += 10 * self.level

            faint_abilities = [
                x for x in self.abilities
                if x.ability_id == AbilityID.FAINT_IN_X_TURNS
            ]
            if faint_abilities:
                faint_abilities[0].turns += self.level

        # Modifier
        if not self.modifier_id and self.level:
            self.modifier_id = choice(list(ModifierID))

        if self.modifier_id == ModifierID.UNNATURALLY_TICKLISH:
            self.name = 'Unnaturally Ticklish ' + self.name
            self.max_st -= 5 if not one_dmg else 1
        if self.modifier_id == ModifierID.TOUGH:
            self.name = 'Tough ' + self.name
            self.max_ep += 2
        if self.modifier_id == ModifierID.BIG:
            if 'Big' in self.name:
                self.name = self.name.replace('Big', 'Gargantuan')
            elif 'Small' in self.name:
                self.name = self.name.replace('Small', 'Not So Small')
            else:
                self.name = 'Big ' + self.name
            self.max_st += 20 if not one_dmg else 2
            self.max_ep += 1
        if self.modifier_id == ModifierID.MISCHIEVOUS:
            self.name = 'Mischievous ' + self.name
            self.dmg += 10
        if self.modifier_id == ModifierID.BLESSED_BY_LAUGHTER:
            self.name = 'Blessed ' + self.name
            self.abilities.append(Ability(
                AbilityID.HEAL_ST_EVERY_X_HITS,
                heal=(5 if not one_dmg else 1),
                hits=(1 if not one_dmg else 2)))
        if self.modifier_id == ModifierID.CURSED:
            self.name = 'Cursed ' + self.name
            self.abilities.append(Ability(
                AbilityID.CAST_SPELL_EVERY_X_TURNS,
                turns=2))

        # Trinkets
        if not self.trinket_id and self.level and self.level % 3 == 0:
            self.trinket_id = choice(list(TRINKETS))

        if self.trinket_id == ItemID.GRINDSTONE:
            self.dmg += 2
        if self.trinket_id == ItemID.RING_ENDURANCE:
            if self.max_ep <= 0:
                self.max_ep = 1
            self.abilities.append(Ability(
                AbilityID.HEAL_EP_EVERY_X_TURNS,
                heal=1, turns=5))
        if self.trinket_id == ItemID.GOLDEN_FEATHER:
            self.gold += 10
        if self.trinket_id == ItemID.BROKEN_FEATHERARROW:
            self.abilities.append(Ability(
                AbilityID.DAMAGE_AFTER_X_TURNS_ON_HIT,
                dmg_dice=(1, 20), turns=5))
        if self.trinket_id == ItemID.LIQUID_LAUGHTER_VIAL:
            self.abilities.append(Ability(
                AbilityID.INFLICT_STATUS_ON_HIT,
                status_id=StatusID.LGI, level=1))
        if self.trinket_id == ItemID.SWIFT_FEATHER:
            self.abilities.append(Ability(
                AbilityID.CHANCE_TO_EVADE,
                chance_dice=(1, 10), target=10))

        # Final stats
        self.st = self.max_st
        self.ep = self.max_ep
