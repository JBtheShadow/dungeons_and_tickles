from __future__ import annotations

from enum import Enum, auto

from ability import Ability, AbilityID
from enemy import Enemy, ModifierID
from reward import Reward, RewardID
from trap import Trap, TrapID


class EncounterID(Enum):
    ORC = auto()
    GOBLIN = auto()
    KOBOLD = auto()
    FLYING_TICKLE_IMPS = auto()
    TICKLE_TRAP = auto()
    SMALL_TICKLE_SLIME = auto()
    GARGOYLE = auto()
    VINE_MONSTER = auto()
    CHEST_MIMIC = auto()
    NOTHING = auto()
    BIG_RAT = auto()
    TWIN_TAILED_SNAKE = auto()
    BIG_TICKLE_SLIME = auto()
    SKELETON = auto()
    ITEM = auto()
    LICH = auto()
    TICKLE_ZOMBIE = auto()
    MUMMY = auto()
    DRAGONBORN = auto()
    BLACK_MAGE = auto()
    CERBERUS = auto()
    TREASURE_ROOM = auto()


class Encounter:
    def __init__(self, encounter_class, *args, **kwargs):
        self.encounter_class = encounter_class
        self.args = args
        self.kwargs = kwargs


ENCOUNTERS = {
    EncounterID.ORC: Encounter(Enemy, "Orc", max_st=50, dmg=10),
    EncounterID.GOBLIN: Encounter(Enemy, "Goblin", max_st=30, dmg=15),
    EncounterID.KOBOLD: Encounter(Enemy, "Kobold", max_st=35, dmg=15),
    EncounterID.FLYING_TICKLE_IMPS: Encounter(
        Enemy,
        "Flying Tickle Imps",
        max_st=25,
        dmg=15,
        abilities=[
            Ability(AbilityID.DAMAGE_EVERY_X_TURNS, dmg_dice=(2, 20), turns=5),
        ],
    ),
    EncounterID.TICKLE_TRAP: Encounter(
        Trap, "Tickle Trap", TrapID.DIRECT_DAMAGE, dmg=25
    ),
    EncounterID.SMALL_TICKLE_SLIME: Encounter(
        Enemy, "Small Tickle Slime", max_st=25, dmg=10
    ),
    EncounterID.GARGOYLE: Encounter(Enemy, "Gargoyle", max_st=50, dmg=10),
    EncounterID.VINE_MONSTER: Encounter(
        Enemy,
        "Vine Monster",
        max_st=5,
        dmg=15,
        abilities=[Ability(AbilityID.ALL_DAMAGE_TAKEN_SET_TO_1)],
    ),
    EncounterID.CHEST_MIMIC: Encounter(
        Enemy,
        "Chest Mimic",
        dmg=30,
        abilities=[Ability(AbilityID.FAINT_IN_X_TURNS, turns=5)],
    ),
    EncounterID.NOTHING: Encounter(None),
    EncounterID.BIG_RAT: Encounter(Enemy, "Big Rat", max_st=15, dmg=10),
    EncounterID.TWIN_TAILED_SNAKE: Encounter(
        Enemy, "Twin-Tailed Snake", max_st=10, dmg=20
    ),
    EncounterID.BIG_TICKLE_SLIME: Encounter(
        Enemy, "Big Tickle Slime", max_st=30, dmg=20
    ),
    EncounterID.SKELETON: Encounter(
        Enemy,
        "Skeleton",
        max_st=25,
        dmg=15,
        abilities=[Ability(AbilityID.IMMUNE_EVERY_X_TURNS, turns=2)],
    ),
    EncounterID.ITEM: Encounter(Reward, RewardID.ITEM),
    EncounterID.LICH: Encounter(Enemy, "Lich", max_st=50, dmg=25),
    EncounterID.TICKLE_ZOMBIE: Encounter(
        Enemy,
        "Tickle Zombie",
        max_st=40,
        dmg=10,
    ),
    EncounterID.MUMMY: Encounter(Enemy, "Mummy", max_st=30, dmg=15),
    EncounterID.DRAGONBORN: Encounter(
        Enemy,
        "Dragonborn",
        max_st=50,
        dmg=20,
        abilities=[
            Ability(AbilityID.DAMAGE_EVERY_X_TURNS, dmg_dice=(3, 6), turns=5),
            Ability(AbilityID.FIXED_DAMAGE_ON_PLAYER_MISS, dmg=5),
        ],
    ),
    EncounterID.BLACK_MAGE: Encounter(
        Enemy,
        "Black Mage",
        max_st=15,
        dmg=35,
        abilities=[
            Ability(AbilityID.DAMAGE_EVERY_X_TURNS, dmg_dice=(1, 10), turns=5),
        ],
    ),
    EncounterID.CERBERUS: Encounter(
        Enemy,
        "Cerberus",
        max_st=30,
        dmg=15,
        abilities=[
            Ability(AbilityID.FIXED_DAMAGE_EVERY_X_HITS, dmg=5, hits=3),
        ],
    ),
    EncounterID.TREASURE_ROOM: Encounter(
        Reward, RewardID.GOLD_AND_TRINKET, gold_dice=(2, 20, 60)
    ),
}


# Testing
if __name__ == "__main__":
    from helpers import dice_roll, dice_roll_advantage, print_dice
    from item import ITEMS

    enemy_enc = ENCOUNTERS[EncounterID.DRAGONBORN]
    enemy = enemy_enc.encounter_class(
        *enemy_enc.args,
        level=1,
        **enemy_enc.kwargs,
    )
    print(enemy)

    trap_enc = ENCOUNTERS[EncounterID.TICKLE_TRAP]
    trap = trap_enc.encounter_class(*trap_enc.args, **trap_enc.kwargs)
    print(trap)

    reward_enc = ENCOUNTERS[EncounterID.ITEM]
    reward = reward_enc.encounter_class(*reward_enc.args, **reward_enc.kwargs)
    print(reward)

    small_slime_enc = ENCOUNTERS[EncounterID.SMALL_TICKLE_SLIME]
    big_slime_enc = ENCOUNTERS[EncounterID.BIG_TICKLE_SLIME]

    level = 3
    for enc in [small_slime_enc, big_slime_enc]:
        for modifier_id in [ModifierID.TOUGH, ModifierID.BIG]:
            slime = enc.encounter_class(
                *enc.args, level=level, modifier_id=modifier_id, **enc.kwargs
            )
            trinket = ITEMS[slime.trinket_id]
            print(f"Level {slime.level} {slime.name} holding a {trinket.name}")
            level += 3

    for dice in [(1, 20), (2, 20), (3, 6, 10), (1, 10, -2)]:
        dtext = print_dice(*dice)

        roll = dice_roll(*dice)
        roll_adv = dice_roll_advantage(*dice)

        print(f"{dtext} -> regular roll:", roll)
        print(f"{dtext} -> roll w/ advantage:", roll_adv)
