from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from ability import AbilityID, StatID
from trap import TrapID


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
    curr_actions: int = None
    curr_gold: int = None
    curr_st: int = None
    temp_at: int = None
    temp_ep: int = None
    temp_all: int = None
    set_ep: int = None


@dataclass
class Item:
    name: str
    description: str = None

    ability_id: AbilityID = None
    ability_dmg: int = None
    ability_mod: int = None
    ability_choices: list[Choice] = None

    consumable: bool = False
    once_a_turn: bool = None
    uses: int = None
    curr_st: int = None
    max_st: int = None
    curr_mp: int = None
    max_mp: int = None
    temp_at: int = None
    temp_ep: int = None
    set_ep: int = None
    curr_actions: int = None

    trap: bool = False
    trap_id: TrapID = None
    trap_dmg: int = None
    trap_dmg_dice: tuple = None
    trap_mod: int = None
    trap_mod_stat: StatID = None
    trap_fee: int = None
    trap_ends_turn: bool = None
    trap_challenge: bool = None

    weapon: bool = False
    once_a_combat: bool = None
    ignore_hit_roll: bool = None
    dmg_dice: tuple = None
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

    passive: bool = False

    trinket: bool = False

    def __post_init__(self):
        if self.consumable and self.uses is None:
            self.uses = 1


ITEMS = {
    # Shop items 1-10
    ItemID.SMOKE_BOMB: Item(
        "Smoke Bomb",
        "Escape combat for free",
        consumable=True,
        ability_id=AbilityID.ESCAPE_FROM_BATTLE,
    ),
    ItemID.STAMINA_POTION: Item(
        "Stamina Potion",
        "Restore 30 Stamina",
        consumable=True,
        uses=3,
        curr_st=30,
    ),
    ItemID.MP_POTION: Item(
        "MP Potion",
        "Recover 15 MP",
        consumable=True,
        uses=3,
        curr_mp=15,
    ),
    ItemID.AT_POTION: Item(
        "AT Potion",
        "Gain 3 Temporary AT",
        consumable=True,
        uses=2,
        temp_at=3,
    ),
    ItemID.EP_POTION: Item(
        "EP Potion",
        "Gain 2 Temporary EP",
        consumable=True,
        uses=2,
        temp_ep=2,
    ),
    ItemID.PICKAXE: Item(
        "Pickaxe",
        "Gives a +20 Modifier to rolls in the mines",
        consumable=True,
        uses=10,
        ability_id=AbilityID.MINES_MODIFIER,
        ability_mod=20,
    ),
    ItemID.SMALL_FEATHER_BOMB: Item(
        "Small Feather Bomb",
        "Deals 25 damage to a mob or player",
        consumable=True,
        curr_st=-25,
    ),
    ItemID.TICKLE_TRAP: Item(
        "Tickle Trap",
        "Place it somewhere to force an unsuspecting player "
        "suffer a debuff and take damage",
        consumable=True,
        trap=True,
        trap_id=TrapID.TICKLE_TRAP,
        trap_mod=-10,
        trap_dmg=5,
    ),
    ItemID.TOLLBOOTH: Item(
        "Toolbooth",
        "Place it over somewhere and force other players to pay a "
        "fee if they visit said location\n"
        "Lasts 1 round, any gold collected goes to you",
        consumable=True,
        trap=True,
        trap_id=TrapID.TOLLBOOTH,
        trap_fee=25,
    ),
    ItemID.FEATHER_SWORD: Item(
        "Feather Sword",
        "Increases your damage dice to 1d10",
        weapon=True,
        dmg_dice=(1, 10),
        dur=10,
    ),
    # Shop Items 11-20
    ItemID.FEATHER_LONGSWORD: Item(
        "Feather Longsword",
        "Increases your damage dice to 1d10\n" "Sturdier than a regular sword",
        weapon=True,
        dmg_dice=(1, 10),
        dur=20,
    ),
    ItemID.BERSERK_POTION: Item(
        "Berserk Potion",
        "Removes all EP and gives 5 Temporary AT",
        consumable=True,
        uses=2,
        set_ep=0,
        temp_at=5,
    ),
    ItemID.HASTE_POTION: Item(
        "Haste Potion",
        "Gives an additional action, usable only once per turn",
        consumable=True,
        once_a_turn=True,
        uses=3,
        curr_actions=1,
    ),
    ItemID.LUCK_POTION: Item(
        "Luck Potion",
        "Gives a +10 Modifier to any roll",
        consumable=True,
        uses=2,
        ability_id=AbilityID.ANY_ROLL_MODIFIER,
        ability_mod=10,
    ),
    ItemID.BRACELET_ENDURANCE: Item(
        "Bracelet of Endurance",
        "Adds +1 EP for two rounds",
        bracelet=True,
        degradeable=True,
        rounds=2,
        temp_ep=1,
    ),
    ItemID.BRACELET_GREATER_ENDURANCE: Item(
        "Bracelet of Greater Endurance",
        "Adds +2 EP for two rounds",
        bracelet=True,
        degradeable=True,
        rounds=2,
        temp_ep=2,
    ),
    ItemID.BOW: Item(
        "Bow",
        "Deal 1d20+AT damage once per combat without rolling\n",
        "Requires Feather Arrows",
        weapon=True,
        once_a_combat=True,
        ignore_hit_roll=True,
        require_ammo=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
        dmg_dice=(1, 20),
    ),
    ItemID.FEATHERARROW_QUIVER: Item(
        "Feather Arrow Quiver",
        "A pack of 10 Feather Arrows",
        ammo_pack=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
    ),
    ItemID.GREATER_FEATHER_BOMB: Item(
        "Greater Feather Bomb",
        "Deals 50 damage to a mob or player",
        consumable=True,
        curr_st=-50,
    ),
    ItemID.POTION_VERSATILITY: Item(
        "Potion of Versatility",
        "Gives 1 Temporary AT and EP\n"
        "Heals for 25 ST\n"
        "Gives you a +5 Modifier for the whole battle\n"
        "Modifier non stackable",
        consumable=True,
        curr_st=25,
        temp_at=1,
        temp_ep=1,
        ability_id=AbilityID.UNSTACKABLE_BATTLE_MODIFIER,
        ability_mod=5,
    ),
    # Shop Items 21-30
    ItemID.POTION_CONSTITUTION: Item(
        "Potion of Constitution",
        "Increases Max ST by 15",
        consumable=True,
        max_st=15,
    ),
    ItemID.POTION_FOCUS: Item(
        "Potion of Focus",
        "Increases Max MP by 15",
        consumable=True,
        max_mp=15,
    ),
    ItemID.BOOK_TICKLISH_CURSES: Item(
        "Book of Ticklish Curses",
        "Once a turn choose one of the following to happen:\n"
        "- Make a player lose an action and 5 ST\n"
        "- Make a player lose 20G and 10 ST\n"
        "- Reduce all stats by 1 temporarily and 5 ST\n"
        "- Reduce all EP and 10 ST\n",
        consumable=True,
        once_a_turn=True,
        uses=5,
        ability_id=AbilityID.CHOOSE_ONE,
        ability_choices=[
            Choice(
                "An action and 5 ST",
                curr_actions=-1,
                curr_st=-5,
            ),
            Choice(
                "20G and 10 ST",
                curr_gold=-20,
                curr_st=-10,
            ),
            Choice(
                "All stats -1 temporarily and 5 ST",
                temp_all=-1,
                curr_st=-5,
            ),
            Choice(
                "All EP and 10 ST",
                set_ep=0,
                curr_st=-10,
            ),
        ],
    ),
    ItemID.FEATHER: Item(
        "Feather",
        "Tickle an opponent making them lose 1 action and 10 ST",
        consumable=True,
        once_a_turn=True,
        uses=3,
        curr_actions=-1,
        curr_st=-10,
    ),
    ItemID.TICKLE_GLUE_TRAP: Item(
        "Tickle Glue Trap",
        "Place it in a location making any player who tries to enter it "
        "lose their turn and take 10 ST of damage",
        consumable=True,
        trap=True,
        trap_id=TrapID.TICKLE_GLUE_TRAP,
        trap_dmg=10,
        trap_ends_turn=True,
    ),
    ItemID.PENDULUM: Item(
        "Pendulum",
        "Hypnotize a player to visit a location on their turn",
        consumable=True,
        ability_id=AbilityID.FORCE_MOVE_TO_LOCATION,
    ),
    ItemID.MAGIC_BOOK: Item(
        "Magic Book",
        "Teaches a new spell on use. No rerolling!",
        consumable=True,
        uses=3,
        ability_id=AbilityID.LEARN_NEW_SPELL,
    ),
    ItemID.SCRAP_METAL: Item(
        "Scrap Metal",
        "Collect three of these to craft an item of your choice, " "free of charge!",
        stackable=True,
    ),
    ItemID.TRIPWIRE: Item(
        "Tripwire",
        "Allows for a chance to steal from another player " "if they trigger the trap",
        consumable=True,
        trap=True,
        trap_id=TrapID.TRIPWIRE,
        trap_challenge=True,
        trap_dmg_dice=(1, 6),
        trap_mod_stat=StatID.AT,
    ),
    ItemID.FOUR_LEAF_CLOVER: Item(
        "Four Leaf Clover",
        "Adds +2 to all rolls excluding damage, peacock, "
        "item and spell rolls. Doesn't stack with itself",
        passive=True,
        ability_id=AbilityID.UNSTACKABLE_MISC_MODIFIER,
    ),
    # Shop Items 31-40
    ItemID.FEATHER_SPEAR: Item(
        "Feather Spear",
        "Increases your damage dice from 1d6 to 1d12",
        weapon=True,
        dmg_dice=(1, 12),
        dur=10,
    ),
    ItemID.PINWHEEL_AXE: Item(
        "Pinwheel Ace",
        "Increases your damage dice from 1d6 to 1d20",
        weapon=True,
        dmg_dice=(1, 20),
        dur=5,
    ),
    # Ammo
    ItemID.FEATHERARROW: Item(
        "Feather Arrow",
        "Ammunition for the bow",
        ammo=True,
    ),
    # Trinkets
    ItemID.GRINDSTONE: Item("Grindstone", "", trinket=True),
    ItemID.RING_ENDURANCE: Item("Ring of Endurance", "", trinket=True),
    ItemID.GOLDEN_FEATHER: Item("Golden Feather", "", trinket=True),
    ItemID.BROKEN_FEATHERARROW: Item("Broken Featherarrow", "", trinket=True),
    ItemID.LIQUID_LAUGHTER_VIAL: Item("Liquid Laughter Vial", "", trinket=True),
    ItemID.SWIFT_FEATHER: Item("Swift Feather", "", trinket=True),
}


TRINKETS = {
    ItemID.GRINDSTONE,
    ItemID.RING_ENDURANCE,
    ItemID.GOLDEN_FEATHER,
    ItemID.BROKEN_FEATHERARROW,
    ItemID.LIQUID_LAUGHTER_VIAL,
    ItemID.SWIFT_FEATHER,
}
