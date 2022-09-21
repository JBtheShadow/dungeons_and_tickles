from __future__ import annotations
from enum import Enum, auto

from enemy import Enemy, EnemyAbility, EnemyAbilityId, ModifierId
from reward import Reward, RewardId
from trap import Trap, TrapType


class EncounterId(Enum):
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
    EncounterId.ORC:
        Encounter(Enemy, 'Orc', max_st=50, dmg=10),
    EncounterId.GOBLIN:
        Encounter(Enemy, 'Goblin', max_st=30, dmg=15),
    EncounterId.KOBOLD:
        Encounter(Enemy, 'Kobold', max_st=35, dmg=15),
    EncounterId.FLYING_TICKLE_IMPS:
        Encounter(Enemy, 'Flying Tickle Imps', max_st=25, dmg=15, abilities=[
            EnemyAbility(EnemyAbilityId.DAMAGE_EVERY_X_TURNS,
                         dmg_dice=(2, 20), turns=5)
        ]),
    EncounterId.TICKLE_TRAP:
        Encounter(Trap, 'Tickle Trap', TrapType.DIRECT_DAMAGE, dmg=25),
    EncounterId.SMALL_TICKLE_SLIME:
        Encounter(Enemy, 'Small Tickle Slime', max_st=25, dmg=10),
    EncounterId.GARGOYLE:
        Encounter(Enemy, 'Gargoyle', max_st=50, dmg=10),
    EncounterId.VINE_MONSTER:
        Encounter(Enemy, 'Vine Monster', max_st=5, dmg=15, abilities=[
            EnemyAbility(EnemyAbilityId.ALL_DAMAGE_TAKEN_SET_TO_1)
        ]),
    EncounterId.CHEST_MIMIC:
        Encounter(Enemy, 'Chest Mimic', dmg=30, abilities=[
            EnemyAbility(EnemyAbilityId.FAINT_IN_X_TURNS,
                         turns=5)
        ]),
    EncounterId.NOTHING:
        Encounter(None),
    EncounterId.BIG_RAT:
        Encounter(Enemy, 'Big Rat', max_st=15, dmg=10),
    EncounterId.TWIN_TAILED_SNAKE:
        Encounter(Enemy, 'Twin-Tailed Snake', max_st=10, dmg=20),
    EncounterId.BIG_TICKLE_SLIME:
        Encounter(Enemy, 'Big Tickle Slime', max_st=30, dmg=20),
    EncounterId.SKELETON:
        Encounter(Enemy, 'Skeleton', max_st=25, dmg=15, abilities=[
            EnemyAbility(EnemyAbilityId.IMMUNE_EVERY_X_TURNS,
                         turns=2)
        ]),
    EncounterId.ITEM:
        Encounter(Reward, RewardId.ITEM),
    EncounterId.LICH:
        Encounter(Enemy, 'Lich', max_st=50, dmg=25),
    EncounterId.TICKLE_ZOMBIE:
        Encounter(Enemy, 'Tickle Zombie', max_st=40, dmg=10),
    EncounterId.MUMMY:
        Encounter(Enemy, 'Mummy', max_st=30, dmg=15),
    EncounterId.DRAGONBORN:
        Encounter(Enemy, 'Dragonborn', max_st=50, dmg=20, abilities=[
            EnemyAbility(EnemyAbilityId.DAMAGE_EVERY_X_TURNS,
                         dmg_dice=(3, 6), turns=5),
            EnemyAbility(EnemyAbilityId.FIXED_DAMAGE_ON_PLAYER_MISS,
                         dmg=5)
        ]),
    EncounterId.BLACK_MAGE:
        Encounter(Enemy, 'Black Mage', max_st=15, dmg=35, abilities=[
            EnemyAbility(EnemyAbilityId.DAMAGE_EVERY_X_TURNS,
                         dmg_dice=(1, 10), turns=5)
        ]),
    EncounterId.CERBERUS:
        Encounter(Enemy, 'Cerberus', max_st=30, dmg=15, abilities=[
            EnemyAbility(EnemyAbilityId.FIXED_DAMAGE_EVERY_X_HITS,
                         dmg=5, hits=3)
        ]),
    EncounterId.TREASURE_ROOM:
        Encounter(Reward, RewardId.GOLD_AND_TRINKET,
                  gold_dice=(2, 20, 60))
}


# Testing
if __name__ == '__main__':
    from item import TRINKETS
    from helpers import dice_roll, dice_roll_advantage, print_dice

    enemy_enc = ENCOUNTERS[EncounterId.DRAGONBORN]
    enemy = enemy_enc.encounter_class(
        *enemy_enc.args, level=1, **enemy_enc.kwargs
    )
    print(enemy)

    trap_enc = ENCOUNTERS[EncounterId.TICKLE_TRAP]
    trap = trap_enc.encounter_class(
        *trap_enc.args, **trap_enc.kwargs
    )
    print(trap)

    reward_enc = ENCOUNTERS[EncounterId.ITEM]
    reward = reward_enc.encounter_class(
        *reward_enc.args, **reward_enc.kwargs
    )
    print(reward)

    small_slime_enc = ENCOUNTERS[EncounterId.SMALL_TICKLE_SLIME]
    big_slime_enc = ENCOUNTERS[EncounterId.BIG_TICKLE_SLIME]

    level = 3
    for enc in [small_slime_enc, big_slime_enc]:
        for modifier_id in [ModifierId.TOUGH, ModifierId.BIG]:
            slime = enc.encounter_class(
                *enc.args, level=level, modifier_id=modifier_id, **enc.kwargs
            )
            trinket = TRINKETS[slime.trinket_id]
            print(f'Level {slime.level} {slime.name} holding a {trinket.name}')
            level += 3

    for dice in [(1, 20), (2, 20), (3, 6, 10), (1, 10, -2)]:
        dtext = print_dice(*dice)

        roll = dice_roll(*dice)
        roll_adv = dice_roll_advantage(*dice)

        print(f'{dtext} -> regular roll:', roll)
        print(f'{dtext} -> roll w/ advantage:', roll_adv)
