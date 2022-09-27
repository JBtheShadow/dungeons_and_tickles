from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from ability import AbilityID
from dice import Dice, RollModifierType
from trap import TrapID


class ItemID(Enum):
    # Special items
    MAGIC_WAND = auto()

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
    STOCKS_TELEPORTER = auto()

    # Enhanced Potions
    ENHANCED_STAMINA_POTION = auto()
    ENHANCED_MP_POTION = auto()
    ENHANCED_AT_POTION = auto()
    ENHANCED_EP_POTION = auto()
    ENHANCED_BERSERK_POTION = auto()
    ENHANCED_HASTE_POTION = auto()
    ENHANCED_LUCK_POTION = auto()
    ENHANCED_VERSATILITY_POTION = auto()
    ENHANCED_CONSTITUTION_POTION = auto()
    ENHANCED_FOCUS_POTION = auto()

    # Ammo
    FEATHERARROW = auto()

    # Other
    USED_UP_KOBOLD_PLUSHIE = auto()

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


class ItemTransformType(Enum):
    ENHANCE = auto()
    FINAL_USE = auto()


@dataclass
class ItemInfo:
    item_id: ItemID
    name: str
    description: str

    ability_id: AbilityID = None

    transform_type: ItemTransformType = None
    transform_id: ItemID = None

    consumable: bool = False
    once_a_turn: bool = None
    only_one: bool = None
    uses: int = None
    heal_st: int = None
    heal_st_perc: float = None
    max_st: int = None
    heal_mp: int = None
    max_mp: int = None
    bonus_at: int = None
    bonus_ep: int = None
    set_ep: int = None
    heal_actions: int = None

    trap_id: TrapID = None

    weapon: bool = False
    swift: bool = None
    double_hit: bool = None
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

    item_shop: bool = False

    def __post_init__(self):
        if self.consumable and self.uses is None:
            self.uses = 1

    @staticmethod
    def from_id(item_id: ItemID):
        return _ITEMS[item_id]


_ITEMS = {
    # Shop items 1-10
    ItemID.SMOKE_BOMB: ItemInfo(
        item_id=ItemID.SMOKE_BOMB,
        name="Smoke Bomb",
        description="Escape combat for free",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.SMOKE_BOMB,
    ),
    ItemID.STAMINA_POTION: ItemInfo(
        item_id=ItemID.STAMINA_POTION,
        name="Stamina Potion",
        description="Restore 30 Stamina",
        item_shop=True,
        consumable=True,
        uses=3,
        heal_st=30,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_STAMINA_POTION,
    ),
    ItemID.MP_POTION: ItemInfo(
        item_id=ItemID.MP_POTION,
        name="MP Potion",
        description="Recover 15 MP",
        item_shop=True,
        consumable=True,
        uses=3,
        heal_mp=15,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_MP_POTION,
    ),
    ItemID.AT_POTION: ItemInfo(
        item_id=ItemID.AT_POTION,
        name="AT Potion",
        description="Gain 3 Temporary AT",
        item_shop=True,
        consumable=True,
        uses=2,
        bonus_at=3,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_AT_POTION,
    ),
    ItemID.EP_POTION: ItemInfo(
        item_id=ItemID.EP_POTION,
        name="EP Potion",
        description="Gain 2 Temporary EP",
        item_shop=True,
        consumable=True,
        uses=2,
        bonus_ep=2,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_EP_POTION,
    ),
    ItemID.PICKAXE: ItemInfo(
        item_id=ItemID.PICKAXE,
        name="Pickaxe",
        description="Gives a +20 Modifier to rolls in the mines",
        item_shop=True,
        consumable=True,
        uses=10,
        ability_id=AbilityID.PICKAXE,
    ),
    ItemID.SMALL_FEATHER_BOMB: ItemInfo(
        item_id=ItemID.SMALL_FEATHER_BOMB,
        name="Small Feather Bomb",
        description="Deals 25 damage to a mob or player",
        item_shop=True,
        consumable=True,
        heal_st=-25,
    ),
    ItemID.TICKLE_TRAP: ItemInfo(
        item_id=ItemID.TICKLE_TRAP,
        name="Tickle Trap",
        description="Place it somewhere to force an unsuspecting player "
        "suffer a debuff and take damage",
        item_shop=True,
        consumable=True,
        trap_id=TrapID.TICKLE_TRAP,
    ),
    ItemID.TOLLBOOTH: ItemInfo(
        item_id=ItemID.TOLLBOOTH,
        name="Toolbooth",
        description="Place it over somewhere and force other players to pay a "
        "fee if they visit said location\n"
        "Lasts 1 round, any gold collected goes to you",
        item_shop=True,
        consumable=True,
        trap_id=TrapID.TOLLBOOTH,
    ),
    ItemID.FEATHER_SWORD: ItemInfo(
        item_id=ItemID.FEATHER_SWORD,
        name="Feather Sword",
        description="Sets your damage dice to 1d10",
        item_shop=True,
        weapon=True,
        dmg_dice=Dice(sides=10),
        dur=10,
    ),
    # Shop Items 11-20
    ItemID.FEATHER_LONGSWORD: ItemInfo(
        item_id=ItemID.FEATHER_LONGSWORD,
        name="Feather Longsword",
        description="Sets your damage dice to 1d10\n" "Sturdier than a regular sword",
        item_shop=True,
        weapon=True,
        dmg_dice=Dice(sides=10),
        dur=20,
    ),
    ItemID.BERSERK_POTION: ItemInfo(
        item_id=ItemID.BERSERK_POTION,
        name="Berserk Potion",
        description="Removes all EP and gives 5 Temporary AT",
        item_shop=True,
        consumable=True,
        uses=2,
        set_ep=0,
        bonus_at=5,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_BERSERK_POTION,
    ),
    ItemID.HASTE_POTION: ItemInfo(
        item_id=ItemID.HASTE_POTION,
        name="Haste Potion",
        description="Gives an additional action, usable only once per turn",
        item_shop=True,
        consumable=True,
        once_a_turn=True,
        uses=3,
        heal_actions=1,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_HASTE_POTION,
    ),
    ItemID.LUCK_POTION: ItemInfo(
        item_id=ItemID.LUCK_POTION,
        name="Luck Potion",
        description="Gives a +10 Modifier to any roll",
        item_shop=True,
        consumable=True,
        uses=2,
        ability_id=AbilityID.LUCK_POTION,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_LUCK_POTION,
    ),
    ItemID.BRACELET_ENDURANCE: ItemInfo(
        item_id=ItemID.BRACELET_ENDURANCE,
        name="Bracelet of Endurance",
        description="Adds +1 EP for two rounds",
        item_shop=True,
        bracelet=True,
        degradeable=True,
        rounds=2,
        bonus_ep=1,
    ),
    ItemID.BRACELET_GREATER_ENDURANCE: ItemInfo(
        item_id=ItemID.BRACELET_GREATER_ENDURANCE,
        name="Bracelet of Greater Endurance",
        description="Adds +2 EP for two rounds",
        item_shop=True,
        bracelet=True,
        degradeable=True,
        rounds=2,
        bonus_ep=2,
    ),
    ItemID.BOW: ItemInfo(
        item_id=ItemID.BOW,
        name="Bow",
        description="Deal 1d20+AT damage once per combat without rolling\n"
        "Requires Feather Arrows",
        item_shop=True,
        weapon=True,
        once_a_combat=True,
        ignore_hit_roll=True,
        require_ammo=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
        dmg_dice=Dice(sides=20),
    ),
    ItemID.FEATHERARROW_QUIVER: ItemInfo(
        item_id=ItemID.FEATHERARROW_QUIVER,
        name="Feather Arrow Quiver",
        description="A pack of 10 Feather Arrows",
        item_shop=True,
        ammo_pack=True,
        ammo_item_id=ItemID.FEATHERARROW,
        ammo_count=3,
    ),
    ItemID.GREATER_FEATHER_BOMB: ItemInfo(
        item_id=ItemID.GREATER_FEATHER_BOMB,
        name="Greater Feather Bomb",
        description="Deals 50 damage to a mob or player",
        item_shop=True,
        consumable=True,
        heal_st=-50,
    ),
    ItemID.POTION_VERSATILITY: ItemInfo(
        item_id=ItemID.POTION_VERSATILITY,
        name="Potion of Versatility",
        description="Gives 1 Temporary AT and EP\n"
        "Heals for 25 ST\n"
        "Gives you a +5 Modifier for the whole battle\n"
        "Modifier non stackable",
        item_shop=True,
        consumable=True,
        uses=2,
        heal_st=25,
        bonus_at=1,
        bonus_ep=1,
        ability_id=AbilityID.POTION_VERSATILITY,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_VERSATILITY_POTION,
    ),
    # Shop Items 21-30
    ItemID.POTION_CONSTITUTION: ItemInfo(
        item_id=ItemID.POTION_CONSTITUTION,
        name="Potion of Constitution",
        description="Increases Max ST by 15",
        item_shop=True,
        consumable=True,
        max_st=15,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_CONSTITUTION_POTION,
    ),
    ItemID.POTION_FOCUS: ItemInfo(
        item_id=ItemID.POTION_FOCUS,
        name="Potion of Focus",
        description="Increases Max MP by 15",
        item_shop=True,
        consumable=True,
        max_mp=15,
        transform_type=ItemTransformType.ENHANCE,
        transform_id=ItemID.ENHANCED_FOCUS_POTION,
    ),
    ItemID.BOOK_TICKLISH_CURSES: ItemInfo(
        item_id=ItemID.BOOK_TICKLISH_CURSES,
        name="Book of Ticklish Curses",
        description="Once a turn choose one of the following to happen:\n"
        "- Make a player lose an action and 5 ST\n"
        "- Make a player lose 20G and 10 ST\n"
        "- Reduce all stats by 1 temporarily and 5 ST\n"
        "- Reduce all EP and 10 ST\n",
        item_shop=True,
        consumable=True,
        once_a_turn=True,
        uses=5,
        ability_id=AbilityID.BOOK_TICKLISH_CURSES,
    ),
    ItemID.FEATHER: ItemInfo(
        item_id=ItemID.FEATHER,
        name="Feather",
        description="Tickle an opponent making them lose 1 action and 10 ST",
        item_shop=True,
        consumable=True,
        once_a_turn=True,
        uses=3,
        heal_actions=-1,
        heal_st=-10,
    ),
    ItemID.TICKLE_GLUE_TRAP: ItemInfo(
        item_id=ItemID.TICKLE_GLUE_TRAP,
        name="Tickle Glue Trap",
        description="Place it in a location making any player who tries to enter it "
        "lose their turn and take 10 ST of damage",
        item_shop=True,
        consumable=True,
        trap_id=TrapID.TICKLE_GLUE_TRAP,
    ),
    ItemID.PENDULUM: ItemInfo(
        item_id=ItemID.PENDULUM,
        name="Pendulum",
        description="Hypnotize a player to visit a location on their turn",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.PENDULUM,
    ),
    ItemID.MAGIC_BOOK: ItemInfo(
        item_id=ItemID.MAGIC_BOOK,
        name="Magic Book",
        description="Teaches a new spell on use. No rerolling!",
        item_shop=True,
        consumable=True,
        uses=3,
        ability_id=AbilityID.MAGIC_BOOK,
    ),
    ItemID.SCRAP_METAL: ItemInfo(
        item_id=ItemID.SCRAP_METAL,
        name="Scrap Metal",
        description="Collect three of these to craft an item of your choice, "
        "free of charge!",
        item_shop=True,
        stackable=True,
    ),
    ItemID.TRIPWIRE: ItemInfo(
        item_id=ItemID.TRIPWIRE,
        name="Tripwire",
        description="Allows for a chance to steal from another player "
        "if they trigger the trap",
        item_shop=True,
        consumable=True,
        trap_id=TrapID.TRIPWIRE,
    ),
    ItemID.FOUR_LEAF_CLOVER: ItemInfo(
        item_id=ItemID.FOUR_LEAF_CLOVER,
        name="Four Leaf Clover",
        description="Adds +2 to all rolls excluding damage, peacock, "
        "item and spell rolls. Doesn't stack with itself",
        item_shop=True,
        passive=True,
        ability_id=AbilityID.FOUR_LEAF_CLOVER,
    ),
    # Shop Items 31-40
    ItemID.FEATHER_SPEAR: ItemInfo(
        item_id=ItemID.FEATHER_SPEAR,
        name="Feather Spear",
        description="Increases your damage dice from 1d6 to 1d12",
        item_shop=True,
        weapon=True,
        dmg_dice=Dice(sides=12),
        dur=10,
    ),
    ItemID.PINWHEEL_AXE: ItemInfo(
        item_id=ItemID.PINWHEEL_AXE,
        name="Pinwheel Ace",
        description="Increases your damage dice from 1d6 to 1d20",
        item_shop=True,
        weapon=True,
        dmg_dice=Dice(sides=20),
        dur=5,
    ),
    ItemID.AMULET_PROTECTION: ItemInfo(
        item_id=ItemID.AMULET_PROTECTION,
        name="Amulet of Protection",
        description="Negate any attempts to trap, curse, tickle or debuff you "
        "from other players or enemies",
        item_shop=True,
        accessory=True,
        dur=3,
        ability_id=AbilityID.AMULET_PROTECTION,
    ),
    ItemID.NECKLACE_FORTUNE: ItemInfo(
        item_id=ItemID.NECKLACE_FORTUNE,
        name="Necklace of Fortune",
        description="Increase gold gained from defeating monsters",
        item_shop=True,
        passive=True,
        ability_id=AbilityID.NECKLACE_FORTUNE,
    ),
    ItemID.STIRRUPS_STEALTH: ItemInfo(
        item_id=ItemID.STIRRUPS_STEALTH,
        name="Stirrups of Stealth",
        description="Allow you to bypass an enemy encounter and move up a floor",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.STIRRUPS_STEALTH,
    ),
    ItemID.POTION_ENHANCER: ItemInfo(
        item_id=ItemID.POTION_ENHANCER,
        name="Potion Enhancer",
        description="Improves the effects of a potion",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.POTION_ENHANCER,
    ),
    ItemID.VIP_MINE_PASS: ItemInfo(
        item_id=ItemID.VIP_MINE_PASS,
        name="VIP Mine Pass",
        description="Gain double gold from the mines for one round",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.VIP_MINE_PASS,
    ),
    ItemID.LUCKY_COIN: ItemInfo(
        item_id=ItemID.LUCKY_COIN,
        name="Lucky Coin",
        description="Reroll a failed dice roll once\n"
        "Afterwards, your next three dice rolls are increased by 2",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.LUCKY_COIN,
    ),
    ItemID.WYLDSAP: ItemInfo(
        item_id=ItemID.WYLDSAP,
        name="Wyldsap",
        description="Heal 1/4 of your ST",
        item_shop=True,
        consumable=True,
        uses=2,
        heal_st_perc=0.25,
    ),
    ItemID.RIGGED_DIE: ItemInfo(
        item_id=ItemID.RIGGED_DIE,
        name="Rigged Die",
        description="Set the die of any result you desire, "
        "can be used on other players' turns as well",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.RIGGED_DIE,
    ),
    # Shop Items 41-49
    ItemID.FEATHAGGER: ItemInfo(
        item_id=ItemID.FEATHAGGER,
        name="Feathagger",
        description="Deal 1d6 + half of your AT as a bonus action",
        item_shop=True,
        weapon=True,
        swift=True,
        dur=15,
        dmg_dice=Dice(modifier_type=RollModifierType.HALF_AT),
    ),
    ItemID.DOUBLE_FEATHAGGERS: ItemInfo(
        item_id=ItemID.DOUBLE_FEATHAGGERS,
        name="Double Feathaggers",
        description="Deal 1d4 + AT twice whenever you hit with an attack",
        item_shop=True,
        weapon=True,
        double_hit=True,
        dur=10,
        dmg_dice=Dice(sides=4, modifier_type=RollModifierType.AT),
    ),
    ItemID.PIGGYBANK: ItemInfo(
        item_id=ItemID.PIGGYBANK,
        name="Piggybank",
        description="Prevents item loss and lets you keep half of your gold "
        "whenever the user faints. Gets destroyed afterwards",
        item_shop=True,
        passive=True,
        ability_id=AbilityID.PIGGYBANK,
    ),
    ItemID.PEACOCK_POTION: ItemInfo(
        item_id=ItemID.PEACOCK_POTION,
        name="Peacock Potion",
        description="You start laughing, feeling your most ticklish spots "
        "get tickled by feathers. May curse or bless you with the same "
        "effects granted by the Magical Peacock",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.PEACOCK_POTION,
    ),
    ItemID.KOBOLD_PLUSHIE: ItemInfo(
        item_id=ItemID.KOBOLD_PLUSHIE,
        name="Kobold Plushie",
        description="Simply tickle a part of the plushie's body and think of "
        "who you wish affect. Remove 1 EP or deal 1d10+AT damage to the "
        "afflicted player in addition to one of the effects below:\n"
        " - Ribs/pits: target temporarily loses half of their AT\n"
        " - Belly/sides: target loses half of their EP\n"
        " - Legs/feet: target losts 1 action on their turn\n"
        "After the three uses are up you may keep the plushie as a dummy item",
        item_shop=True,
        consumable=True,
        uses=3,
        transform_type=ItemTransformType.FINAL_USE,
        transform_id=ItemID.USED_UP_KOBOLD_PLUSHIE,
        ability_id=AbilityID.KOBOLD_PLUSHIE,
    ),
    ItemID.HEADBAND_RETRIBUTION: ItemInfo(
        item_id=ItemID.HEADBAND_RETRIBUTION,
        name="Headband of Retribution",
        description="Returns half the ST damage taken back to the attacker",
        item_shop=True,
        consumable=True,
        uses=3,
        ability_id=AbilityID.HEADBAND_RETRIBUTION,
    ),
    ItemID.ANKLET_RETRIBUTION: ItemInfo(
        item_id=ItemID.ANKLET_RETRIBUTION,
        name="Anklet of Retribution",
        description="Returns 1/10 of the ST damage taken back to the attacker. "
        "Magic prevents carrying multiples of this item",
        item_shop=True,
        passive=True,
        only_one=True,
        ability_id=AbilityID.ANKLET_RETRIBUTION,
    ),
    ItemID.CAMPING_EQUIPMENT: ItemInfo(
        item_id=ItemID.CAMPING_EQUIPMENT,
        name="Camping Equipment",
        description="May be used after defeating a monster at the dungeon to "
        "restore 1/2 of your ST, MP and 1 EP. Allows for an extra fight at no "
        "action cost. Comes with a ration, a tent, a totally not mimic bedroll "
        "and a blanket!",
        item_shop=True,
        consumable=True,
        ability_id=AbilityID.CAMPING_EQUIPMENT,
    ),
    ItemID.STOCKS_TELEPORTER: ItemInfo(
        item_id=ItemID.STOCKS_TELEPORTER,
        name="Stocks Teleporter",
        description="When a player visits a location roll against the trapper "
        "to check if they see an almost invisible gray pad on the floor which "
        "when stepped on teleports the target to the public stocks\n"
        "Targets on the public stocks have to spend 2 actions to get out and "
        "are dealt 15 ST damage as they're tickled by the town inhabitants. "
        "Lacking actions, they remain stuck until their next turn.\n"
        "Other players are welcome to spend an action and deal 1d6+AT to the "
        "stuck player, while the trapper can do so at no cost.\n"
        "Players in the public stocks may be tickled by anyone without "
        "incurring any faith penalties",
        item_shop=True,
        consumable=True,
        trap_id=TrapID.STOCKS_TELEPORTER,
    ),
    # Ammo
    ItemID.FEATHERARROW: ItemInfo(
        item_id=ItemID.FEATHERARROW,
        name="Feather Arrow",
        description="Ammunition for the bow",
        ammo=True,
    ),
    # Other
    ItemID.USED_UP_KOBOLD_PLUSHIE: ItemInfo(
        item_id=ItemID.USED_UP_KOBOLD_PLUSHIE,
        name="Used Up Kobold Plushie",
        description="You can tickle them if you want but it won't really do "
        "anything in this state. Maybe you can pretend it still has a use",
    ),
    # Enhanced Potions
    ItemID.ENHANCED_STAMINA_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_STAMINA_POTION,
        name="Enhanced Stamina Potion",
        description="Restore 60 Stamina",
        consumable=True,
        uses=2,
        heal_st=60,
    ),
    ItemID.ENHANCED_MP_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_MP_POTION,
        name="Enhanced MP Potion",
        description="Recover 30 MP",
        consumable=True,
        uses=2,
        heal_mp=30,
    ),
    ItemID.ENHANCED_AT_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_AT_POTION,
        name="Enhanced AT Potion",
        description="Gain 6 Temporary AT",
        consumable=True,
        bonus_at=6,
    ),
    ItemID.ENHANCED_EP_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_EP_POTION,
        name="Enhanced EP Potion",
        description="Gain 4 Temporary EP",
        consumable=True,
        uses=2,
        bonus_ep=2,
    ),
    ItemID.ENHANCED_BERSERK_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_BERSERK_POTION,
        name="Enhanced Berserk Potion",
        description="Removes all EP and gives 10 Temporary AT",
        consumable=True,
        set_ep=0,
        bonus_at=10,
    ),
    ItemID.ENHANCED_HASTE_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_HASTE_POTION,
        name="Enhanced Haste Potion",
        description="Gives two additional actions, usable only once per turn",
        consumable=True,
        once_a_turn=True,
        heal_actions=2,
    ),
    ItemID.ENHANCED_LUCK_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_LUCK_POTION,
        name="Luck Potion",
        description="Gives a +15 Modifier to any non attack roll or makes "
        "an attack hit automatically",
        consumable=True,
        ability_id=AbilityID.ENHANCED_LUCK_POTION,
    ),
    ItemID.ENHANCED_VERSATILITY_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_VERSATILITY_POTION,
        name="Enhanced Versatility Potion",
        description="Gives 2 Temporary AT and EP\n"
        "Heals for 50 ST\n"
        "Gives your rolls advantage for the whole battle\n"
        "Modifier non stackable",
        consumable=True,
        heal_st=50,
        bonus_at=2,
        bonus_ep=2,
        ability_id=AbilityID.ENHANCED_VERSATILITY_POTION,
    ),
    ItemID.ENHANCED_CONSTITUTION_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_CONSTITUTION_POTION,
        name="Enhanced Constitution Potion",
        description="Increases Max ST by 30",
        consumable=True,
        max_st=30,
    ),
    ItemID.ENHANCED_FOCUS_POTION: ItemInfo(
        item_id=ItemID.ENHANCED_FOCUS_POTION,
        name="Enhanced Focus Potion",
        description="Increases Max MP by 30",
        consumable=True,
        max_mp=30,
    ),
    # Trinkets
    ItemID.GRINDSTONE: ItemInfo(
        item_id=ItemID.GRINDSTONE,
        name="Grindstone",
        description="Boosts AT by 2",
        trinket=True,
    ),
    ItemID.RING_ENDURANCE: ItemInfo(
        item_id=ItemID.RING_ENDURANCE,
        name="Ring of Endurance",
        description="+1 EP restored each round (max of 5)",
        trinket=True,
        ability_id=AbilityID.RING_ENDURANCE,
    ),
    ItemID.GOLDEN_FEATHER: ItemInfo(
        item_id=ItemID.GOLDEN_FEATHER,
        name="Golden Feather",
        description="+10 gold earned from all sources",
        trinket=True,
        ability_id=AbilityID.GOLDEN_FEATHER,
    ),
    ItemID.BROKEN_FEATHERARROW: ItemInfo(
        item_id=ItemID.BROKEN_FEATHERARROW,
        name="Broken Featherarrow",
        description="+1 Feather Arrow each round",
        trinket=True,
        ability_id=AbilityID.BROKEN_FEATHERARROW,
    ),
    ItemID.LIQUID_LAUGHTER_VIAL: ItemInfo(
        item_id=ItemID.LIQUID_LAUGHTER_VIAL,
        name="Liquid Laughter Vial",
        description="1 LGI dealt each successful hit",
        trinket=True,
        ability_id=AbilityID.LIQUID_LAUGHTER_VIAL,
    ),
    ItemID.SWIFT_FEATHER: ItemInfo(
        item_id=ItemID.SWIFT_FEATHER,
        name="Swift Feather",
        description="1 in 10 chance to evade damage",
        trinket=True,
        ability_id=AbilityID.SWIFT_FEATHER,
    ),
}

SHOP_ITEM_IDS = {item_id for item_id, item in _ITEMS.items() if item.item_shop}
TRINKET_IDS = {item_id for item_id, item in _ITEMS.items() if item.trinket}
