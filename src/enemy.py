from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from random import choice

from ability import AbilityID
from item import TRINKET_IDS, ItemID


class EnemyID(Enum):
    ORC = auto()
    GOBLIN = auto()
    KOBOLD = auto()
    FLYING_TICKLE_IMPS = auto()
    SMALL_TICKLE_SLIME = auto()
    GARGOYLE = auto()
    VINE_MONSTER = auto()
    CHEST_MIMIC = auto()
    BIG_RAT = auto()
    TWIN_TAILED_SNAKE = auto()
    BIG_TICKLE_SLIME = auto()
    SKELETON = auto()
    LICH = auto()
    TICKLE_ZOMBIE = auto()
    MUMMY = auto()
    DRAGONBORN = auto()
    BLACK_MAGE = auto()
    CERBERUS = auto()
    TICKLE_SPIDER = auto()


class ModifierID(Enum):
    UNNATURALLY_TICKLISH = auto()
    TOUGH = auto()
    BIG = auto()
    MISCHIEVOUS = auto()
    BLESSED_BY_LAUGHTER = auto()
    CURSED = auto()


@dataclass
class EnemyInfo:
    enemy_id: EnemyID
    name: str
    max_st: int = 0
    max_ep: int = 0
    dmg: int = 0
    undead: bool = False
    demonic: bool = False
    can_master_weapons: bool = False
    ability_ids: list[AbilityID] = field(default_factory=list)

    @staticmethod
    def from_id(enemy_id: EnemyID):
        return _ENEMIES[enemy_id]


@dataclass
class Enemy(EnemyInfo):
    modifier_id: ModifierID = None
    trinket_id: ItemID = None
    level: int = 0
    gold: int = 50

    st: int = field(init=False)
    ep: int = field(init=False)
    countdown: int = field(init=False)

    @staticmethod
    def from_info(info: EnemyInfo, **kwargs: dict):
        return Enemy(**info.__dict__, **kwargs)

    @classmethod
    def from_id(cls, enemy_id: EnemyID, **kwargs: dict):
        info = super().from_id(enemy_id)
        return cls.from_info(info, **kwargs)

    def __post_init__(self):
        self.countdown = 0

        one_dmg = AbilityID.VINE_MONSTER_DAMAGE_RESISTANCE in self.ability_ids

        # Level
        if self.level:
            self.max_st += (10 if not one_dmg else 1) * self.level
            self.dmg += 10 * self.level

            if AbilityID.CHEST_MIMIC_SURVIVAL_BATTLE in self.ability_ids:
                self.countdown = self.level + 5

        # Modifier
        if not self.modifier_id and self.level:
            self.modifier_id = choice(list(ModifierID))

        if self.modifier_id == ModifierID.UNNATURALLY_TICKLISH:
            self.name = "Unnaturally Ticklish " + self.name
            self.max_st -= 5 if not one_dmg else 1
        if self.modifier_id == ModifierID.TOUGH:
            self.name = "Tough " + self.name
            self.max_ep += 2
        if self.modifier_id == ModifierID.BIG:
            if "Big" in self.name:
                self.name = self.name.replace("Big", "Gargantuan")
            elif "Small" in self.name:
                self.name = self.name.replace("Small", "Not So Small")
            else:
                self.name = "Big " + self.name
            self.max_st += 20 if not one_dmg else 2
            self.max_ep += 1
        if self.modifier_id == ModifierID.MISCHIEVOUS:
            self.name = "Mischievous " + self.name
            self.dmg += 10
        if self.modifier_id == ModifierID.BLESSED_BY_LAUGHTER:
            self.name = "Blessed " + self.name
            if one_dmg:
                self.ability_ids.append(AbilityID.BLESSED_VINE_MONSTER)
            else:
                self.ability_ids.append(AbilityID.BLESSED_ENEMY)
        if self.modifier_id == ModifierID.CURSED:
            self.name = "Cursed " + self.name
            self.ability_ids.append(AbilityID.CURSED_ENEMY)

        # Trinkets
        if not self.trinket_id and self.level and self.level % 3 == 0:
            self.trinket_id = choice(list(TRINKET_IDS))

        if self.trinket_id == ItemID.GRINDSTONE:
            self.dmg += 2
        if self.trinket_id == ItemID.RING_ENDURANCE:
            if self.max_ep <= 0:
                self.max_ep = 1
            self.ability_ids.append(AbilityID.RING_ENDURANCE_ENEMY)
        if self.trinket_id == ItemID.GOLDEN_FEATHER:
            self.gold += 10
        if self.trinket_id == ItemID.BROKEN_FEATHERARROW:
            self.ability_ids.append(AbilityID.BROKEN_FEATHERARROW_ENEMY)
        if self.trinket_id == ItemID.LIQUID_LAUGHTER_VIAL:
            self.ability_ids.append(AbilityID.LIQUID_LAUGHTER_VIAL)
        if self.trinket_id == ItemID.SWIFT_FEATHER:
            self.ability_ids.append(AbilityID.SWIFT_FEATHER)

        # Final stats
        self.st = self.max_st
        self.ep = self.max_ep


_ENEMIES = {
    EnemyID.ORC: EnemyInfo(
        enemy_id=EnemyID.ORC, name="Orc", max_st=50, dmg=10, can_master_weapons=True
    ),
    EnemyID.GOBLIN: EnemyInfo(
        enemy_id=EnemyID.GOBLIN,
        name="Goblin",
        max_st=30,
        dmg=15,
        can_master_weapons=True,
    ),
    EnemyID.KOBOLD: EnemyInfo(
        enemy_id=EnemyID.KOBOLD,
        name="Kobold",
        max_st=35,
        dmg=15,
        can_master_weapons=True,
    ),
    EnemyID.FLYING_TICKLE_IMPS: EnemyInfo(
        enemy_id=EnemyID.FLYING_TICKLE_IMPS,
        name="Flying Tickle Imps",
        max_st=25,
        dmg=15,
        demonic=True,
        can_master_weapons=True,
        ability_ids=[AbilityID.FLYING_IMP_TICKLE_RUSH],
    ),
    EnemyID.SMALL_TICKLE_SLIME: EnemyInfo(
        enemy_id=EnemyID.SMALL_TICKLE_SLIME,
        name="Small Tickle Slime",
        max_st=25,
        dmg=10,
    ),
    EnemyID.GARGOYLE: EnemyInfo(
        enemy_id=EnemyID.GARGOYLE,
        name="Gargoyle",
        max_st=50,
        dmg=10,
        demonic=True,
        can_master_weapons=True,
    ),
    EnemyID.VINE_MONSTER: EnemyInfo(
        enemy_id=EnemyID.VINE_MONSTER,
        name="Vine Monster",
        max_st=5,
        dmg=15,
        ability_ids=[AbilityID.VINE_MONSTER_DAMAGE_RESISTANCE],
    ),
    EnemyID.CHEST_MIMIC: EnemyInfo(
        enemy_id=EnemyID.CHEST_MIMIC,
        name="Chest Mimic",
        dmg=30,
        ability_ids=[AbilityID.CHEST_MIMIC_SURVIVAL_BATTLE],
    ),
    EnemyID.BIG_RAT: EnemyInfo(
        enemy_id=EnemyID.BIG_RAT, name="Big Rat", max_st=15, dmg=10
    ),
    EnemyID.TWIN_TAILED_SNAKE: EnemyInfo(
        enemy_id=EnemyID.TWIN_TAILED_SNAKE, name="Twin-Tailed Snake", max_st=10, dmg=20
    ),
    EnemyID.BIG_TICKLE_SLIME: EnemyInfo(
        enemy_id=EnemyID.BIG_TICKLE_SLIME, name="Big Tickle Slime", max_st=30, dmg=20
    ),
    EnemyID.SKELETON: EnemyInfo(
        enemy_id=EnemyID.SKELETON,
        name="Skeleton",
        max_st=25,
        dmg=15,
        undead=True,
        can_master_weapons=True,
        ability_ids=[AbilityID.SKELETON_DAMAGE_IMMUNITY],
    ),
    EnemyID.LICH: EnemyInfo(
        enemy_id=EnemyID.LICH,
        name="Lich",
        max_st=50,
        dmg=25,
        undead=True,
        can_master_weapons=True,
    ),
    EnemyID.TICKLE_ZOMBIE: EnemyInfo(
        enemy_id=EnemyID.TICKLE_ZOMBIE,
        name="Tickle Zombie",
        max_st=40,
        dmg=10,
        undead=True,
    ),
    EnemyID.MUMMY: EnemyInfo(
        enemy_id=EnemyID.MUMMY,
        name="Mummy",
        max_st=30,
        dmg=15,
        undead=True,
        can_master_weapons=True,
    ),
    EnemyID.DRAGONBORN: EnemyInfo(
        enemy_id=EnemyID.DRAGONBORN,
        name="Dragonborn",
        max_st=50,
        dmg=20,
        can_master_weapons=True,
        ability_ids=[AbilityID.DRAGONBORN_BREATH_ATTACK],
    ),
    EnemyID.BLACK_MAGE: EnemyInfo(
        enemy_id=EnemyID.BLACK_MAGE,
        name="Black Mage",
        max_st=15,
        dmg=35,
        ability_ids=[AbilityID.BLACK_MAGE_SPELL],
    ),
    EnemyID.CERBERUS: EnemyInfo(
        enemy_id=EnemyID.CERBERUS,
        name="Cerberus",
        max_st=30,
        dmg=15,
        demonic=True,
        ability_ids=[AbilityID.CERBERUS_TRIPLE_HIT],
    ),
    EnemyID.TICKLE_SPIDER: EnemyInfo(
        enemy_id=EnemyID.TICKLE_SPIDER,
        name="Anthropomorphic Tickle Spider",
        max_st=15,
        dmg=10,
        ability_ids=[AbilityID.TICKLE_SPIDER_WEB],
    ),
}
