from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, auto
from random import choice, randint


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


class ModifierId(Enum):
    UNNATURALLY_TICKLISH = auto()
    TOUGH = auto()
    BIG = auto()
    MISCHIEVOUS = auto()
    BLESSED_BY_LAUGHTER = auto()
    CURSED = auto()


class EnemyAbilityId(Enum):
    ALL_DAMAGE_TAKEN_SET_TO_1 = auto()
    DAMAGE_EVERY_X_TURNS = auto()
    FAINT_IN_X_TURNS = auto()
    IMMUNE_EVERY_X_TURNS = auto()
    FIXED_DAMAGE_EVERY_X_HITS = auto()
    HEAL_ST_EVERY_X_HITS = auto()
    CAST_SPELL_EVERY_X_TURNS = auto()
    FIXED_DAMAGE_ON_PLAYER_MISS = auto()
    HEAL_EP_EVERY_X_TURNS = auto()
    DAMAGE_AFTER_X_TURNS_ON_HIT = auto()
    CHANCE_TO_EVADE = auto()
    INFLICT_STATUS_ON_HIT = auto()


class StatusId(Enum):
    LGI = auto()  # Laughing Gas Intoxication
    TS = auto()   # Ticklish Sensations
    REGEN = auto()
    LRA = auto()  # Laugh Resist Aura
    EVADE = auto()
    BLIND = auto()
    WEAKEN = auto()
    STRENGTHEN = auto()


@dataclass
class Dice:
    number: int
    sides: int
    mod: int = 0

    def roll(self):
        rolls = [
            randint(1, self.sides) for _ in range(self.number)
        ]
        return sum(rolls) + self.mod, rolls


@dataclass
class EnemyAbility:
    ability_id: EnemyAbilityId
    dmg_dice: Dice = None
    status_id: StatusId = None
    chance_dice: Dice = None
    turns: int = None
    dmg: int = None
    heal: int = None
    hits: int = None
    target: int = None
    level: int = None


@dataclass
class Enemy:
    name: str
    max_st: int = None
    max_ep: int = 0
    dmg: int = None
    modifier_id: ModifierId = None
    trinket_id: TrinketId = None
    abilities: list[EnemyAbility] = None
    level: int = 0
    gold: int = 50

    st: int = field(init=False)
    ep: int = field(init=False)

    def __post_init__(self):
        self.abilities = self.abilities or []
        one_dmg = EnemyAbilityId.ALL_DAMAGE_TAKEN_SET_TO_1 in self.abilities

        # Level
        if self.level:
            self.max_st += (10 if not one_dmg else 1) * self.level
            self.dmg += 10 * self.level

            faint_abilities = [
                x for x in self.abilities
                if x.ability_id == EnemyAbilityId.FAINT_IN_X_TURNS
            ]
            if faint_abilities:
                faint_abilities[0].turns += self.level

        # Modifier
        if not self.modifier_id and self.level:
            self.modifier_id = choice(list(ModifierId))

        if self.modifier_id == ModifierId.UNNATURALLY_TICKLISH:
            self.name = 'Unnaturally Ticklish ' + self.name
            self.max_st -= 5 if not one_dmg else 1
        if self.modifier_id == ModifierId.TOUGH:
            self.name = 'Tough ' + self.name
            self.max_ep += 2
        if self.modifier_id == ModifierId.BIG:
            if 'Big' in self.name:
                self.name = self.name.replace('Big', 'Gargantuan')
            elif 'Small' in self.name:
                self.name = self.name.replace('Small', 'Not So Small')
            else:
                self.name = 'Big ' + self.name
            self.max_st += 20 if not one_dmg else 2
            self.max_ep += 1
        if self.modifier_id == ModifierId.MISCHIEVOUS:
            self.name = 'Mischievous ' + self.name
            self.dmg += 10
        if self.modifier_id == ModifierId.BLESSED_BY_LAUGHTER:
            self.name = 'Blessed ' + self.name
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.HEAL_ST_EVERY_X_HITS,
                heal=(5 if not one_dmg else 1),
                hits=(1 if not one_dmg else 2)))
        if self.modifier_id == ModifierId.CURSED:
            self.name = 'Cursed ' + self.name
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.CAST_SPELL_EVERY_X_TURNS,
                turns=2))

        # Trinkets
        if not self.trinket_id and self.level and self.level % 3 == 0:
            self.trinket_id = choice(list(TrinketId))

        if self.trinket_id == TrinketId.GRINDSTONE:
            self.dmg += 2
        if self.trinket_id == TrinketId.RING_ENDURANCE:
            if self.max_ep <= 0:
                self.max_ep = 1
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.HEAL_EP_EVERY_X_TURNS,
                heal=1, turns=5))
        if self.trinket_id == TrinketId.GOLDEN_FEATHER:
            self.gold += 10
        if self.trinket_id == TrinketId.BROKEN_FEATHERARROW:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.DAMAGE_AFTER_X_TURNS_ON_HIT,
                Dice(1, 20), turns=5))
        if self.trinket_id == TrinketId.LIQUID_LAUGHTER_VIAL:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.INFLICT_STATUS_ON_HIT,
                status_id=StatusId.LGI, level=1))
        if self.trinket_id == TrinketId.SWIFT_FEATHER:
            self.abilities.append(EnemyAbility(
                EnemyAbilityId.CHANCE_TO_EVADE,
                chance_dice=Dice(1, 10), target=10))

        # Final stats
        self.st = self.max_st
        self.ep = self.max_ep


class TrapType(Enum):
    DIRECT_DAMAGE = auto()


@dataclass
class Trap:
    name: str
    trap_type: TrapType
    dmg: int = None


class Encounter:
    def __init__(self, encounter_class, *args, **kwargs):
        self.encounter_class = encounter_class
        self.args = args
        self.kwargs = kwargs


class RewardType(Enum):
    ITEM = auto()
    GOLD_AND_TRINKET = auto()


@dataclass
class Reward:
    reward_type: RewardType
    gold_dice: Dice = None


class TrinketId(Enum):
    GRINDSTONE = auto()
    RING_ENDURANCE = auto()
    GOLDEN_FEATHER = auto()
    BROKEN_FEATHERARROW = auto()
    LIQUID_LAUGHTER_VIAL = auto()
    SWIFT_FEATHER = auto()


@dataclass
class Trinket:
    name: str


TRINKETS = {
    TrinketId.GRINDSTONE:
        Trinket('Grindstone'),
    TrinketId.RING_ENDURANCE:
        Trinket('Ring of Endurance'),
    TrinketId.GOLDEN_FEATHER:
        Trinket('Golden Feather'),
    TrinketId.BROKEN_FEATHERARROW:
        Trinket('Broken Featherarrow'),
    TrinketId.LIQUID_LAUGHTER_VIAL:
        Trinket('Liquid Laughter Vial'),
    TrinketId.SWIFT_FEATHER:
        Trinket('Swift Feather'),
}


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
                         Dice(2, 20), turns=5)
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
        Encounter(Reward, RewardType.ITEM),
    EncounterId.LICH:
        Encounter(Enemy, 'Lich', max_st=50, dmg=25),
    EncounterId.TICKLE_ZOMBIE:
        Encounter(Enemy, 'Tickle Zombie', max_st=40, dmg=10),
    EncounterId.MUMMY:
        Encounter(Enemy, 'Mummy', max_st=30, dmg=15),
    EncounterId.DRAGONBORN:
        Encounter(Enemy, 'Dragonborn', max_st=50, dmg=20, abilities=[
            EnemyAbility(EnemyAbilityId.DAMAGE_EVERY_X_TURNS,
                         Dice(3, 6), turns=5),
            EnemyAbility(EnemyAbilityId.FIXED_DAMAGE_ON_PLAYER_MISS,
                         dmg=5)
        ]),
    EncounterId.BLACK_MAGE:
        Encounter(Enemy, 'Black Mage', max_st=15, dmg=35, abilities=[
            EnemyAbility(EnemyAbilityId.DAMAGE_EVERY_X_TURNS,
                         Dice(1, 10), turns=5)
        ]),
    EncounterId.CERBERUS:
        Encounter(Enemy, 'Cerberus', max_st=30, dmg=15, abilities=[
            EnemyAbility(EnemyAbilityId.FIXED_DAMAGE_EVERY_X_HITS,
                         dmg=5, hits=3)
        ]),
    EncounterId.TREASURE_ROOM:
        Encounter(Reward, RewardType.GOLD_AND_TRINKET,
                  gold_dice=Dice(2, 20, 60))
}

# Testing
if __name__ == '__main__':
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
