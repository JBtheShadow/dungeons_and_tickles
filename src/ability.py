from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class AbilityID(Enum):

    # Item abilities
    SMOKE_BOMB = auto()
    PICKAXE = auto()
    LUCK_POTION = auto()
    ENHANCED_LUCK_POTION = auto()
    POTION_VERSATILITY = auto()
    ENHANCED_VERSATILITY_POTION = auto()
    BOOK_TICKLISH_CURSES = auto()
    PENDULUM = auto()
    MAGIC_BOOK = auto()
    FOUR_LEAF_CLOVER = auto()
    AMULET_PROTECTION = auto()
    NECKLACE_FORTUNE = auto()
    STIRRUPS_STEALTH = auto()
    POTION_ENHANCER = auto()
    VIP_MINE_PASS = auto()
    LUCKY_COIN = auto()
    RIGGED_DIE = auto()
    PIGGYBANK = auto()
    PEACOCK_POTION = auto()
    KOBOLD_PLUSHIE = auto()
    HEADBAND_RETRIBUTION = auto()
    ANKLET_RETRIBUTION = auto()
    CAMPING_EQUIPMENT = auto()

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
    AbilityID.ENHANCED_LUCK_POTION: AbilityInfo(
        ability_id=AbilityID.ENHANCED_LUCK_POTION,
        name="Enhanced Luck Potion Effect",
        description="+15 Modifier to any non attack roll or makes "
        "an attack hit automatically",
    ),
    AbilityID.POTION_VERSATILITY: AbilityInfo(
        ability_id=AbilityID.POTION_VERSATILITY,
        name="Potion of Versatility Effect",
        description="+5 modifier for whole battle",
    ),
    AbilityID.ENHANCED_VERSATILITY_POTION: AbilityInfo(
        ability_id=AbilityID.ENHANCED_VERSATILITY_POTION,
        name="Potion of Versatility Effect",
        description="Advantage rolls for the whole battle",
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
    AbilityID.STIRRUPS_STEALTH: AbilityInfo(
        ability_id=AbilityID.STIRRUPS_STEALTH,
        name="Stirrups of Stealth Effect",
        description="Allow you to bypass an enemy encounter and move up a floor",
    ),
    AbilityID.POTION_ENHANCER: AbilityInfo(
        ability_id=AbilityID.POTION_ENHANCER,
        name="Potion Enhancer Effect",
        description="Improves the effects of a potion",
    ),
    AbilityID.VIP_MINE_PASS: AbilityInfo(
        ability_id=AbilityID.VIP_MINE_PASS,
        name="VIP Mine Pass Effect",
        description="Gain double gold from the mines for one round",
    ),
    AbilityID.LUCKY_COIN: AbilityInfo(
        ability_id=AbilityID.LUCKY_COIN,
        name="Lucky Coin Effect",
        description="Reroll a failed dice roll once\n"
        "Afterwards, your next three dice rolls are increased by 2",
    ),
    AbilityID.RIGGED_DIE: AbilityInfo(
        ability_id=AbilityID.RIGGED_DIE,
        name="Rigged Die Effect",
        description="Set the die of any result you desire, "
        "can be used on other players' turns as well",
    ),
    AbilityID.PIGGYBANK: AbilityInfo(
        ability_id=AbilityID.PIGGYBANK,
        name="Piggybank Effect",
        description="Prevents item loss and lets you keep half of your gold "
        "whenever the user faints. Gets destroyed afterwards",
    ),
    AbilityID.PEACOCK_POTION: AbilityInfo(
        ability_id=AbilityID.PEACOCK_POTION,
        name="Peacock Potion Effect",
        description="You start laughing, feeling your most ticklish spots "
        "get tickled by feathers. May curse or bless you with the same "
        "effects granted by the Magical Peacock",
    ),
    AbilityID.KOBOLD_PLUSHIE: AbilityInfo(
        ability_id=AbilityID.KOBOLD_PLUSHIE,
        name="Kobold Plushie Effect",
        description="Simply tickle a part of the plushie's body and think of "
        "who you wish affect. Remove 1 EP or deal 1d10+AT damage to the "
        "afflicted player in addition to one of the effects below:\n"
        " - Ribs/pits: target temporarily loses half of their AT\n"
        " - Belly/sides: target loses half of their EP\n"
        " - Legs/feet: target losts 1 action on their turn\n"
        "After the three uses are up you may keep the plushie as a dummy item",
    ),
    AbilityID.HEADBAND_RETRIBUTION: AbilityInfo(
        ability_id=AbilityID.HEADBAND_RETRIBUTION,
        name="Headband of Retribution Effect",
        description="Returns half the ST damage taken back to the attacker",
    ),
    AbilityID.ANKLET_RETRIBUTION: AbilityInfo(
        ability_id=AbilityID.ANKLET_RETRIBUTION,
        name="Anklet of Retribution Effect",
        description="Returns 1/10 the ST damage taken back to the attacker",
    ),
    AbilityID.CAMPING_EQUIPMENT: AbilityInfo(
        ability_id=AbilityID.CAMPING_EQUIPMENT,
        name="Camping Equipment Effect",
        description="May be used after defeating a monster at the dungeon to "
        "restore 1/2 of your ST, MP and 1 EP. Allows for an extra fight at no "
        "action cost",
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
