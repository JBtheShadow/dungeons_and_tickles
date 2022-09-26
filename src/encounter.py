from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from enemy import EnemyID, EnemyInfo, ModifierID
from reward import RewardID, RewardInfo
from trap import TrapID, TrapInfo


class EncounterType(Enum):
    NOTHING = auto()
    ENEMY = auto()
    TRAP = auto()
    REWARD = auto()


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
    TICKLE_SPIDER = auto()
    TREASURE_ROOM = auto()


@dataclass
class EncounterInfo:
    encounter_id: EncounterID
    encounter_type: EncounterType
    enemy: EnemyInfo = None
    trap: TrapInfo = None
    reward: RewardInfo = None


ENCOUNTERS = {
    EncounterID.ORC: EncounterInfo(
        EncounterID.ORC, EncounterType.ENEMY, enemy=EnemyInfo.from_id(EnemyID.ORC)
    ),
    EncounterID.GOBLIN: EncounterInfo(
        EncounterID.GOBLIN, EncounterType.ENEMY, enemy=EnemyInfo.from_id(EnemyID.GOBLIN)
    ),
    EncounterID.KOBOLD: EncounterInfo(
        EncounterID.KOBOLD, EncounterType.ENEMY, enemy=EnemyInfo.from_id(EnemyID.KOBOLD)
    ),
    EncounterID.FLYING_TICKLE_IMPS: EncounterInfo(
        EncounterID.FLYING_TICKLE_IMPS,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.FLYING_TICKLE_IMPS),
    ),
    EncounterID.TICKLE_TRAP: EncounterInfo(
        EncounterID.TICKLE_TRAP,
        EncounterType.TRAP,
        trap=TrapInfo.from_id(TrapID.DUNGEON_TICKLE_TRAP),
    ),
    EncounterID.SMALL_TICKLE_SLIME: EncounterInfo(
        EncounterID.SMALL_TICKLE_SLIME,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.SMALL_TICKLE_SLIME),
    ),
    EncounterID.GARGOYLE: EncounterInfo(
        EncounterID.GARGOYLE,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.GARGOYLE),
    ),
    EncounterID.VINE_MONSTER: EncounterInfo(
        EncounterID.VINE_MONSTER,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.VINE_MONSTER),
    ),
    EncounterID.CHEST_MIMIC: EncounterInfo(
        EncounterID.CHEST_MIMIC,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.CHEST_MIMIC),
    ),
    EncounterID.NOTHING: EncounterInfo(EncounterID.NOTHING, EncounterType.NOTHING),
    EncounterID.BIG_RAT: EncounterInfo(
        EncounterID.BIG_RAT,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.BIG_RAT),
    ),
    EncounterID.TWIN_TAILED_SNAKE: EncounterInfo(
        EncounterID.TWIN_TAILED_SNAKE,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.TWIN_TAILED_SNAKE),
    ),
    EncounterID.BIG_TICKLE_SLIME: EncounterInfo(
        EncounterID.BIG_TICKLE_SLIME,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.BIG_TICKLE_SLIME),
    ),
    EncounterID.SKELETON: EncounterInfo(
        EncounterID.SKELETON,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.SKELETON),
    ),
    EncounterID.ITEM: EncounterInfo(
        EncounterID.ITEM, EncounterType.REWARD, reward=RewardInfo.from_id(RewardID.ITEM)
    ),
    EncounterID.LICH: EncounterInfo(
        EncounterID.LICH, EncounterType.ENEMY, enemy=EnemyInfo.from_id(EnemyID.LICH)
    ),
    EncounterID.TICKLE_ZOMBIE: EncounterInfo(
        EncounterID.TICKLE_ZOMBIE,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.TICKLE_ZOMBIE),
    ),
    EncounterID.MUMMY: EncounterInfo(
        EncounterID.MUMMY, EncounterType.ENEMY, enemy=EnemyInfo.from_id(EnemyID.MUMMY)
    ),
    EncounterID.DRAGONBORN: EncounterInfo(
        EncounterID.DRAGONBORN,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.DRAGONBORN),
    ),
    EncounterID.BLACK_MAGE: EncounterInfo(
        EncounterID.BLACK_MAGE,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.BLACK_MAGE),
    ),
    EncounterID.CERBERUS: EncounterInfo(
        EncounterID.CERBERUS,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.CERBERUS),
    ),
    EncounterID.TICKLE_SPIDER: EncounterInfo(
        EncounterID.TICKLE_SPIDER,
        EncounterType.ENEMY,
        enemy=EnemyInfo.from_id(EnemyID.TICKLE_SPIDER),
    ),
    EncounterID.TREASURE_ROOM: EncounterInfo(
        EncounterID.TREASURE_ROOM,
        EncounterType.REWARD,
        reward=RewardInfo.from_id(RewardID.GOLD_AND_TRINKET),
    ),
}


# Testing
if __name__ == "__main__":
    from dice import Dice
    from enemy import Enemy
    from item import ItemInfo

    enemy = Enemy.from_id(EnemyID.DRAGONBORN, level=1)
    print(enemy)

    trap_enc = ENCOUNTERS[EncounterID.TICKLE_TRAP]
    trap = trap_enc.trap
    print(trap)

    reward_enc = ENCOUNTERS[EncounterID.ITEM]
    reward = reward_enc.reward
    print(reward)

    level = 3
    for enemy_id in [
        EnemyID.SMALL_TICKLE_SLIME,
        EnemyID.BIG_TICKLE_SLIME,
        EnemyID.BIG_RAT,
    ]:
        for modifier_id in [ModifierID.TOUGH, ModifierID.BIG]:
            enemy2 = Enemy.from_id(enemy_id, level=level, modifier_id=modifier_id)
            trinket = ItemInfo.from_id(enemy2.trinket_id)
            print(f"Level {enemy2.level} {enemy2.name} holding a {trinket.name}")
            level += 3

    hit_dice = Dice(sides=20)
    for dice in [
        Dice(sides=20),
        Dice(number=2, sides=20),
        Dice(number=3, modifier=10),
        Dice(sides=10, modifier=-2),
    ]:
        print(f"{dice} -> hit roll:", hit_dice.roll_hit())
        print(f"{dice} -> hit roll w/ advantage:", hit_dice.roll_advantage())
        print(f"{dice} -> hit w/ disadvantage:", hit_dice.roll_disadvantage())
        print(f"{dice} -> damage roll:", dice.roll_damage())

    dmg = Dice(modifier=4)
    enemy_dmg = 15

    player_st = 100
    enemy_st = 50

    def roll_hits(dice: Dice = Dice(sides=20)):
        while True:
            a = dice.roll_hit()
            b = dice.roll_hit()
            if a != b:
                return a, b

    print("=" * 80)
    print(f"Player at {player_st} ST vs Enemy at {enemy_st} ST")
    round = 1
    while True:
        print("=" * 80)
        print(f"Round {round}, Player at {player_st} ST, Enemy at {enemy_st} ST")

        # Player's turn
        player, enemy = roll_hits()

        print("Player attacks the Enemy")
        print(f"Player rolls {player}")
        print(f"Enemy rolls {enemy}")
        if player.nat_crit and enemy.nat_miss:
            print("Player immediately wins!")
            break
        elif player.nat_miss and enemy.nat_crit:
            print("Player immediately loses!")
            break
        elif player < enemy:
            print("Player missed!")
        else:
            player_dmg = dmg.roll_damage()
            print(f"Player damage: {dmg} = {player_dmg}")
            points = player_dmg.sum * (2 if player.nat_crit else 1)
            enemy_st -= points
            print(f"Player dealt {points} damage!")
            if enemy_st <= 0:
                print("Enemy fainted! Player wins!")
                break
            else:
                print(f"Enemy now has {enemy_st} ST")

        print("-" * 80)
        # Enemy's turn
        enemy, player = roll_hits()

        print("Enemy attacks the Player")
        print(f"Enemy rolls {enemy}")
        print(f"Player rolls {player}")
        if player.nat_crit and enemy.nat_miss:
            print("Player immediately wins!")
            break
        elif player.nat_miss and enemy.nat_crit:
            print("Player immediately loses!")
            break
        elif player > enemy:
            print("Enemy missed!")
        else:
            print(f"Enemy damage: {enemy_dmg}")
            points = enemy_dmg * (2 if enemy.nat_crit else 1)
            player_st -= points
            print(f"Enemy dealt {points} damage!")
            if player_st <= 0:
                print("Player fainted! Player loses!")
                break
            else:
                print(f"Player now has {player_st} ST")

        round += 1
