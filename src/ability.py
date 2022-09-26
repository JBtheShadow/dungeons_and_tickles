from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

# class StatID(Enum):
#     AT = auto()


# class StatusID(Enum):
#     LGI = auto()  # Laughing Gas Intoxication
#     TS = auto()  # Ticklish Sensations
#     REGEN = auto()
#     LRA = auto()  # Laugh Resist Aura
#     EVADE = auto()
#     BLIND = auto()
#     WEAKEN = auto()
#     STRENGTHEN = auto()


class AbilityID(Enum):

    # Item abilities
    SMOKE_BOMB = auto()
    PICKAXE = auto()
    LUCK_POTION = auto()
    POTION_VERSATILITY = auto()
    BOOK_TICKLISH_CURSES = auto()
    PENDULUM = auto()
    MAGIC_BOOK = auto()
    FOUR_LEAF_CLOVER = auto()
    AMULET_PROTECTION = auto()
    NECKLACE_FORTUNE = auto()

    # Enemy abilities
    FLYING_IMP_TICKLE_RUSH = auto()
    VINE_MONSTER_DAMAGE_RESISTANCE = auto()
    CHEST_MIMIC_SURVIVAL_BATTLE = auto()
    SKELETON_DAMAGE_IMMUNITY = auto()
    DRAGONBORN_BREATH_ATTACK = auto()
    BLACK_MAGE_SPELL = auto()
    CERBERUS_TRIPLE_HIT = auto()
    TICKLE_SPIDER_WEB = auto()

    # Modifier abilities
    BLESSED_VINE_MONSTER = auto()
    BLESSED_ENEMY = auto()
    CURSED_ENEMY = auto()

    # Trinket abilities
    GRINDSTONE = auto()
    GOLDEN_FEATHER = auto()
    RING_ENDURANCE = auto()
    RING_ENDURANCE_ENEMY = auto()
    BROKEN_FEATHERARROW = auto()
    BROKEN_FEATHERARROW_ENEMY = auto()
    LIQUID_LAUGHTER_VIAL = auto()
    SWIFT_FEATHER = auto()


@dataclass
class AbilityInfo:
    ability_id: AbilityID
    name: str
    description: str
    # Other attributes temporarily removed
    # while refactoring is in process

    @staticmethod
    def from_id(ability_id: AbilityID):
        return _ABILITIES[ability_id]


_ABILITIES = {
    # Item abilities
    AbilityID.SMOKE_BOMB: AbilityInfo(
        ability_id=AbilityID.SMOKE_BOMB,
        name="Smoke Bomb Effect",
        description="Escape combat for free",
    ),
    AbilityID.PICKAXE: AbilityInfo(
        ability_id=AbilityID.PICKAXE,
        name="Pickaxe Effect",
        description="+20 modifier to rolls over the mines",
    ),
    AbilityID.LUCK_POTION: AbilityInfo(
        ability_id=AbilityID.LUCK_POTION,
        name="Luck Potion Effect",
        description="+10 modifier to any roll",
    ),
    AbilityID.POTION_VERSATILITY: AbilityInfo(
        ability_id=AbilityID.POTION_VERSATILITY,
        name="Potion of Versatility Effect",
        description="+5 modifier for whole battle",
    ),
    AbilityID.BOOK_TICKLISH_CURSES: AbilityInfo(
        ability_id=AbilityID.BOOK_TICKLISH_CURSES,
        name="Book of Ticklish Curses Effect",
        description="Choose one of a couple effects:\n"
        "- Make a player lose an action and 5 ST\n"
        "- Make a player lose 20G and 10 ST\n"
        "- Reduce all stats by 1 temporarily and 5 ST\n"
        "- Reduce all EP and 10 ST\n",
    ),
    AbilityID.PENDULUM: AbilityInfo(
        ability_id=AbilityID.PENDULUM,
        name="Pendulum Effect",
        description="Force player to move to a location on their turn",
    ),
    AbilityID.MAGIC_BOOK: AbilityInfo(
        ability_id=AbilityID.MAGIC_BOOK,
        name="Magic Book Effect",
        description="Teaches a new spell on use. No rerolling!",
    ),
    AbilityID.FOUR_LEAF_CLOVER: AbilityInfo(
        ability_id=AbilityID.FOUR_LEAF_CLOVER,
        name="Four Leaf Clover Effect",
        description="+2 modifier to any rolls excluding damage, peacock, item "
        "or spells",
    ),
    AbilityID.AMULET_PROTECTION: AbilityInfo(
        ability_id=AbilityID.AMULET_PROTECTION,
        name="Amulet of Protection Effect",
        description="Negates attempts to trap, curse, tickle or debuff the player",
    ),
    AbilityID.NECKLACE_FORTUNE: AbilityInfo(
        ability_id=AbilityID.NECKLACE_FORTUNE,
        name="Necklace of Fortune Effect",
        description="Increased gold gained from defeating monsters",
    ),
    # Enemy abilities
    AbilityID.FLYING_IMP_TICKLE_RUSH: AbilityInfo(
        ability_id=AbilityID.FLYING_IMP_TICKLE_RUSH,
        name="Tickle Rush",
        description="2d20 every 5 turns",
    ),
    AbilityID.VINE_MONSTER_DAMAGE_RESISTANCE: AbilityInfo(
        ability_id=AbilityID.VINE_MONSTER_DAMAGE_RESISTANCE,
        name="Damage Resistance",
        description="All damage taken reduced to 1ST",
    ),
    AbilityID.CHEST_MIMIC_SURVIVAL_BATTLE: AbilityInfo(
        ability_id=AbilityID.CHEST_MIMIC_SURVIVAL_BATTLE,
        name="Survival Battle",
        description="Immune to damage, faints automatically after floor+5 turns",
    ),
    AbilityID.SKELETON_DAMAGE_IMMUNITY: AbilityInfo(
        ability_id=AbilityID.SKELETON_DAMAGE_IMMUNITY,
        name="Damage Immunity",
        description="Immune to damage every other turn",
    ),
    AbilityID.DRAGONBORN_BREATH_ATTACK: AbilityInfo(
        ability_id=AbilityID.DRAGONBORN_BREATH_ATTACK,
        name="Breath Attack",
        description="3d6+5 every 5 turns if player rolls lower",
    ),
    AbilityID.BLACK_MAGE_SPELL: AbilityInfo(
        ability_id=AbilityID.BLACK_MAGE_SPELL,
        name="Tickle Spell",
        description="1d10 every 5 turns",
    ),
    AbilityID.CERBERUS_TRIPLE_HIT: AbilityInfo(
        ability_id=AbilityID.CERBERUS_TRIPLE_HIT,
        name="Triple Hit",
        description="5 ST damage every 3 successful hits",
    ),
    AbilityID.TICKLE_SPIDER_WEB: AbilityInfo(
        ability_id=AbilityID.TICKLE_SPIDER_WEB,
        name="Spider Web",
        description="Every 3 turns if the player fails a DC (6+floor) save one of "
        "these events happen:\n"
        "First fail lets the spider's next attack to roll with advantage\n"
        "Second fail lets the spider auto-hit\n"
        "Third fail lets the spider auto-crit\n"
        "Fourth fail forces the player to lose the fight",
    ),
    # Modifier abilities
    AbilityID.BLESSED_VINE_MONSTER: AbilityInfo(
        ability_id=AbilityID.BLESSED_VINE_MONSTER,
        name="Blessed Effect",
        description="Heal 1 ST every other hit",
    ),
    AbilityID.BLESSED_ENEMY: AbilityInfo(
        ability_id=AbilityID.BLESSED_ENEMY,
        name="Blessed Effect",
        description="Heal 5 ST every hit",
    ),
    AbilityID.CURSED_ENEMY: AbilityInfo(
        ability_id=AbilityID.CURSED_ENEMY,
        name="Cursed Effect",
        description="Casts a random spell every 5 turns",
    ),
    # Trinket abilities
    AbilityID.GRINDSTONE: AbilityInfo(
        ability_id=AbilityID.GRINDSTONE,
        name="Grindstone Effect",
        description="Passive +2 AT",
    ),
    AbilityID.GOLDEN_FEATHER: AbilityInfo(
        ability_id=AbilityID.GOLDEN_FEATHER,
        name="Golden Feather Effect",
        description="+10 gold earned from all sources",
    ),
    AbilityID.RING_ENDURANCE: AbilityInfo(
        ability_id=AbilityID.RING_ENDURANCE,
        name="Ring of Endurance Effect",
        description="Heal 1 EP every round if at less than 5",
    ),
    AbilityID.RING_ENDURANCE_ENEMY: AbilityInfo(
        ability_id=AbilityID.RING_ENDURANCE_ENEMY,
        name="Ring of Endurance Effect",
        description="Heal 1 EP every 5 turns",
    ),
    AbilityID.BROKEN_FEATHERARROW: AbilityInfo(
        ability_id=AbilityID.BROKEN_FEATHERARROW,
        name="Broken Featherarrow Effect",
        description="+1 Feather Arrow each round",
    ),
    AbilityID.BROKEN_FEATHERARROW_ENEMY: AbilityInfo(
        ability_id=AbilityID.BROKEN_FEATHERARROW_ENEMY,
        name="Broken Featherarrow Effect",
        description="1d20 damage on hit after 5 turns cooldown",
    ),
    AbilityID.LIQUID_LAUGHTER_VIAL: AbilityInfo(
        ability_id=AbilityID.LIQUID_LAUGHTER_VIAL,
        name="Liquid Laughter Vial Effect",
        description="Applies 1 level of LGI on a successful hit",
    ),
    AbilityID.SWIFT_FEATHER: AbilityInfo(
        ability_id=AbilityID.SWIFT_FEATHER,
        name="Swift Feather Effect",
        description="1 in 10 chance to evade damage",
    ),
}
