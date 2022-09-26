from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from ability import AbilityID, AbilityInfo
from dice import Dice
from trap import TrapID, TrapInfo


class ItemID(Enum):
    # Shop items
    SMOKE_BOMB = auto()
    STAMINA_POTION = auto()
    MP_POTION = auto()
    AT_POTION = auto()
    EP_POTION = auto()
    PICKAXE = auto()
    SMALL_FEATHER_BOMB = auto()
    TICKLE_TRAP = auto()
    TOLLBOOTH = auto()
    FEATHER_SWORD = auto()
    FEATHER_LONGSWORD = auto()
    BERSERK_POTION = auto()
    HASTE_POTION = auto()
    LUCK_POTION = auto()
    BRACELET_ENDURANCE = auto()
    BRACELET_GREATER_ENDURANCE = auto()
    BOW = auto()
    FEATHERARROW_QUIVER = auto()
    GREATER_FEATHER_BOMB = auto()
    POTION_VERSATILITY = auto()
    POTION_CONSTITUTION = auto()
    POTION_FOCUS = auto()
    BOOK_TICKLISH_CURSES = auto()
    FEATHER = auto()
    TICKLE_GLUE_TRAP = auto()
    PENDULUM = auto()
    MAGIC_BOOK = auto()
    SCRAP_METAL = auto()
    TRIPWIRE = auto()
    FOUR_LEAF_CLOVER = auto()
    FEATHER_SPEAR = auto()
    PINWHEEL_AXE = auto()
    AMULET_PROTECTION = auto()
    NECKLACE_FORTUNE = auto()
    STIRRUPS_STEALTH = auto()
    POTION_ENHANCER = auto()
    VIP_MINE_PASS = auto()
    LUCKY_COIN = auto()
    WYLDSAP = auto()
    RIGGED_DIE = auto()
    FEATHAGGER = auto()
    DOUBLE_FEATHAGGERS = auto()
    PIGGYBANK = auto()
    PEACOCK_POTION = auto()
    KOBOLD_PLUSHIE = auto()
    HEADBAND_RETRIBUTION = auto()
    ANKLET_RETRIBUTION = auto()
    CAMPING_EQUIPMENT = auto()

    # Ammo
    FEATHERARROW = auto()

    # Trinkets
    GRINDSTONE = auto()
    RING_ENDURANCE = auto()
    GOLDEN_FEATHER = auto()
    BROKEN_FEATHERARROW = auto()
    LIQUID_LAUGHTER_VIAL = auto()
    SWIFT_FEATHER = auto()


@dataclass
class Choice:
    description: str
    heal_actions: int = None
    curr_gold: int = None
    heal_st: int = None
    bonus_at: int = None
    bonus_ep: int = None
    temp_all: int = None
    set_ep: int = None


@dataclass
class ItemInfo:
    name: str
    description: str

    ability: AbilityInfo = None

    consumable: bool = False
    once_a_turn: bool = None
    uses: int = None
    heal_st: int = None
    max_st: int = None
    heal_mp: int = None
    max_mp: int = None
    bonus_at: int = None
    bonus_ep: int = None
    set_ep: int = None
    heal_actions: int = None

    trap: TrapInfo = None

    weapon: bool = False
    once_a_combat: bool = None
    ignore_hit_roll: bool = None
    dmg_dice: Dice = None
    dur: int = None
    require_ammo: bool = None
    ammo_item_id: ItemID = None
    ammo_count: int = None

    ammo: bool = False
    ammo_pack: bool = False

    bracelet: bool = False
    degradeable: bool = None
    rounds: int = None

    stackable: bool = False

    accessory: bool = False

    passive: bool = False

    trinket: bool = False

    def __post_init__(self):
        if self.consumable and self.uses is None:
            self.uses = 1

    @staticmethod
    def from_id(item_id: ItemID):
        return _ITEMS[item_id]


_ITEMS = {
    # Shop items 1-10
    ItemID.SMOKE_BOMB: ItemInfo(
        "Smoke Bomb",
        "Escape combat for free",
        consumable=True,
        ability=AbilityInfo.from_id(AbilityID.SMOKE_BOMB),
    ),
    ItemID.STAMINA_POTION: ItemInfo(
        "Stamina Potion",
        "Restore 30 Stamina",
        consumable=True,
        uses=3,
        heal_st=30,
    ),
    ItemID.MP_POTION: ItemInfo(
        "MP Potion",
        "Recover 15 MP",
        consumable=True,
        uses=3,
        heal_mp=15,
    ),
    ItemID.AT_POTION: ItemInfo(
        "AT Potion",
        "Gain 3 Temporary AT",
        consumable=True,
        uses=2,
        bonus_at=3,
    ),
    ItemID.EP_POTION: ItemInfo(
        "EP Potion",
        "Gain 2 Temporary EP",
        consumable=True,
        uses=2,
        bonus_ep=2,
    ),
    ItemID.PICKAXE: ItemInfo(
        "Pickaxe",
        "Gives a +20 Modifier to rolls in the mines",
        consumable=True,
        uses=10,
        ability=AbilityInfo.from_id(AbilityID.PICKAXE),
    ),
    ItemID.SMALL_FEATHER_BOMB: ItemInfo(
        "Small Feather Bomb",
        "Deals 25 damage to a mob or player",
        consumable=True,
        heal_st=-25,
    ),
    ItemID.TICKLE_TRAP: ItemInfo(
        "Tickle Trap",
        "Place it somewhere to force an unsuspecting player "
        "suffer a debuff and take damage",
        consumable=True,
        trap=TrapInfo.from_id(TrapID.TICKLE_TRAP),
    ),
    ItemID.TOLLBOOTH: ItemInfo(
        "Toolbooth",
        "Place it over somewhere and force other players to pay a "
        "fee if they visit said location\n"
        "Lasts 1 round, any gold collected goes to you",
        consumable=True,
        trap=TrapInfo.from_id(TrapID.TOLLBOOTH),
    ),
    ItemID.FEATHER_SWORD: ItemInfo(
        "Feather Sword",
        "Increases your damage dice to 1d10",
        weapon=True,
        dmg_dice=Dice(sides=10),
        dur=10,
    ),
    # Shop Items 11-20
    ItemID.FEATHER_LONGSWORD: ItemInfo(
        "Feather Longsword",
        "Increases your damage dice to 1d10\n" "Sturdier than a regular sword",
        weapon=True,
        dmg_dice=Dice(sides=10),
        dur=20,
    ),
    ItemID.BERSERK_POTION: ItemInfo(
        "Berserk Potion",
        "Removes all EP and gives 5 Temporary AT",
        consumable=True,
        uses=2,
        set_ep=0,
        bonus_at=5,
    ),
    ItemID.HASTE_POTION: ItemInfo(
        "Haste Potion",
        "Gives an additional action, usable only once per turn",
        consumable=True,
        once_a_turn=True,
        uses=3,
        heal_actions=1,
    ),
    ItemID.LUCK_POTION: ItemInfo(
        "Luck Potion",
        "Gives a +10 Modifier to any roll",
        consumable=True,
        uses=2,
        ability=AbilityInfo.from_id(AbilityID.LUCK_POTION),
    ),
    ItemID.BRACELET_ENDURANCE: ItemInfo(
        "Bracelet of Endurance",
        "Adds +1 EP for two rounds",
        bracelet=True,
        degradeable=True,
        rounds=2,
        bonus_ep=1,
    ),
    ItemID.BRACELET_GREATER_ENDURANCE: ItemInfo(
        "Bracelet of Greater Endurance",
        "Adds +2 EP for two rounds",
        bracelet=True,
        degradeable=True,
        rounds=2,
        bonus_ep=2,
    ),
    ItemID.BOW: ItemInfo(
        "Bow",
        "Deal 1d20+AT damage once per combat without rolling\n",
        "Requires Feather Arrows",
        weapon=True,
        once_a_combat=True,
        ignore_hit_roll=True,
        require_ammo=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
        dmg_dice=Dice(sides=20),
    ),
    ItemID.FEATHERARROW_QUIVER: ItemInfo(
        "Feather Arrow Quiver",
        "A pack of 10 Feather Arrows",
        ammo_pack=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
    ),
    ItemID.GREATER_FEATHER_BOMB: ItemInfo(
        "Greater Feather Bomb",
        "Deals 50 damage to a mob or player",
        consumable=True,
        heal_st=-50,
    ),
    ItemID.POTION_VERSATILITY: ItemInfo(
        "Potion of Versatility",
        "Gives 1 Temporary AT and EP\n"
        "Heals for 25 ST\n"
        "Gives you a +5 Modifier for the whole battle\n"
        "Modifier non stackable",
        consumable=True,
        heal_st=25,
        bonus_at=1,
        bonus_ep=1,
        ability=AbilityInfo.from_id(AbilityID.POTION_VERSATILITY),
    ),
    # Shop Items 21-30
    ItemID.POTION_CONSTITUTION: ItemInfo(
        "Potion of Constitution",
        "Increases Max ST by 15",
        consumable=True,
        max_st=15,
    ),
    ItemID.POTION_FOCUS: ItemInfo(
        "Potion of Focus",
        "Increases Max MP by 15",
        consumable=True,
        max_mp=15,
    ),
    ItemID.BOOK_TICKLISH_CURSES: ItemInfo(
        "Book of Ticklish Curses",
        "Once a turn choose one of the following to happen:\n"
        "- Make a player lose an action and 5 ST\n"
        "- Make a player lose 20G and 10 ST\n"
        "- Reduce all stats by 1 temporarily and 5 ST\n"
        "- Reduce all EP and 10 ST\n",
        consumable=True,
        once_a_turn=True,
        uses=5,
        ability=AbilityInfo.from_id(AbilityID.BOOK_TICKLISH_CURSES),
    ),
    ItemID.FEATHER: ItemInfo(
        "Feather",
        "Tickle an opponent making them lose 1 action and 10 ST",
        consumable=True,
        once_a_turn=True,
        uses=3,
        heal_actions=-1,
        heal_st=-10,
    ),
    ItemID.TICKLE_GLUE_TRAP: ItemInfo(
        "Tickle Glue Trap",
        "Place it in a location making any player who tries to enter it "
        "lose their turn and take 10 ST of damage",
        consumable=True,
        trap=TrapInfo.from_id(TrapID.TICKLE_GLUE_TRAP),
    ),
    ItemID.PENDULUM: ItemInfo(
        "Pendulum",
        "Hypnotize a player to visit a location on their turn",
        consumable=True,
        ability=AbilityInfo.from_id(AbilityID.PENDULUM),
    ),
    ItemID.MAGIC_BOOK: ItemInfo(
        "Magic Book",
        "Teaches a new spell on use. No rerolling!",
        consumable=True,
        uses=3,
        ability=AbilityInfo.from_id(AbilityID.MAGIC_BOOK),
    ),
    ItemID.SCRAP_METAL: ItemInfo(
        "Scrap Metal",
        "Collect three of these to craft an item of your choice, " "free of charge!",
        stackable=True,
    ),
    ItemID.TRIPWIRE: ItemInfo(
        "Tripwire",
        "Allows for a chance to steal from another player " "if they trigger the trap",
        consumable=True,
        trap=TrapInfo.from_id(TrapID.TRIPWIRE),
    ),
    ItemID.FOUR_LEAF_CLOVER: ItemInfo(
        "Four Leaf Clover",
        "Adds +2 to all rolls excluding damage, peacock, "
        "item and spell rolls. Doesn't stack with itself",
        passive=True,
        ability=AbilityInfo.from_id(AbilityID.FOUR_LEAF_CLOVER),
    ),
    # Shop Items 31-40
    ItemID.FEATHER_SPEAR: ItemInfo(
        "Feather Spear",
        "Increases your damage dice from 1d6 to 1d12",
        weapon=True,
        dmg_dice=Dice(sides=12),
        dur=10,
    ),
    ItemID.PINWHEEL_AXE: ItemInfo(
        "Pinwheel Ace",
        "Increases your damage dice from 1d6 to 1d20",
        weapon=True,
        dmg_dice=Dice(sides=20),
        dur=5,
    ),
    ItemID.AMULET_PROTECTION: ItemInfo(
        "Amulet of Protection",
        "Negate any attempts to trap, curse, tickle or debuff you "
        "from other players or enemies",
        accessory=True,
        dur=3,
        ability=AbilityInfo.from_id(AbilityID.AMULET_PROTECTION),
    ),
    ItemID.NECKLACE_FORTUNE: ItemInfo(
        "Necklace of Fortune",
        "Increase gold gained from defeating monsters",
        passive=True,
        ability=AbilityInfo.from_id(AbilityID.NECKLACE_FORTUNE),
    ),
    # Ammo
    ItemID.FEATHERARROW: ItemInfo(
        "Feather Arrow",
        "Ammunition for the bow",
        ammo=True,
    ),
    # Trinkets
    ItemID.GRINDSTONE: ItemInfo("Grindstone", "", trinket=True),
    ItemID.RING_ENDURANCE: ItemInfo("Ring of Endurance", "", trinket=True),
    ItemID.GOLDEN_FEATHER: ItemInfo("Golden Feather", "", trinket=True),
    ItemID.BROKEN_FEATHERARROW: ItemInfo("Broken Featherarrow", "", trinket=True),
    ItemID.LIQUID_LAUGHTER_VIAL: ItemInfo("Liquid Laughter Vial", "", trinket=True),
    ItemID.SWIFT_FEATHER: ItemInfo("Swift Feather", "", trinket=True),
}


TRINKETS = {
    ItemID.GRINDSTONE,
    ItemID.RING_ENDURANCE,
    ItemID.GOLDEN_FEATHER,
    ItemID.BROKEN_FEATHERARROW,
    ItemID.LIQUID_LAUGHTER_VIAL,
    ItemID.SWIFT_FEATHER,
}
