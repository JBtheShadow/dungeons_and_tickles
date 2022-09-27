from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from random import randint


class RollModifierType(Enum):
    FLAT = auto()
    AT = auto()
    HALF_AT = auto()


@dataclass
class Dice:
    number: int = 1
    sides: int = 6
    modifier: int = 0
    modifier_type: RollModifierType = RollModifierType.FLAT
    needs_modifier: bool = field(init=False, repr=False)

    def __post_init__(self):
        self.needs_modifier = self.modifier_type == RollModifierType.FLAT

    def __str__(self) -> str:
        if self.modifier > 0:
            return f"{self.number}d{self.sides}+{self.modifier}"
        elif self.modifier < 0:
            return f"{self.number}d{self.sides}{self.modifier}"
        else:
            return f"{self.number}d{self.sides}"

    def roll_hit(self):
        rolls = [randint(1, self.sides) for _ in range(self.number)]
        return DiceRoll(
            sum=sum(rolls) + self.modifier,
            rolls=rolls,
            nat_crit=self.sides in rolls,
            nat_miss=1 in rolls,
        )

    def roll_damage(self):
        rolls = [randint(1, self.sides) for _ in range(self.number)]
        return DiceRoll(sum=sum(rolls) + self.modifier, rolls=rolls)

    def roll_advantage(self):
        rolls = [[randint(1, self.sides) for _ in range(2)] for _ in range(self.number)]
        rolls_adv = [max(r) for r in rolls]
        crits = len([1 for n in rolls_adv if n == self.sides])
        misses = len([1 for n in rolls_adv if n == 1])
        return DiceRoll(
            sum=sum(rolls_adv) + self.modifier,
            rolls=rolls_adv,
            rolls_ext=rolls,
            nat_crit=crits > misses,
            nat_miss=misses > crits,
        )

    def roll_disadvantage(self):
        rolls = [[randint(1, self.sides) for _ in range(2)] for _ in range(self.number)]
        rolls_dis = [min(r) for r in rolls]
        crits = len([1 for n in rolls_dis if n == self.sides])
        misses = len([1 for n in rolls_dis if n == 1])
        return DiceRoll(
            sum=sum(rolls_dis) + self.modifier,
            rolls=rolls_dis,
            rolls_ext=rolls,
            nat_crit=crits > misses,
            nat_miss=misses > crits,
        )


@dataclass(order=True)
class DiceRoll:
    sum: int = 0
    nat_crit: bool = False
    nat_miss: bool = False
    rolls: list[int] = field(default_factory=list[int])
    rolls_ext: list[list[int]] = None

    def __str__(self) -> str:
        hit_or_miss = ""
        if self.nat_crit:
            hit_or_miss = " (CRIT!)"
        elif self.nat_miss:
            hit_or_miss = " (Miss...)"

        if self.rolls_ext:
            return f"{self.sum}{hit_or_miss} {self.rolls}; {self.rolls_ext}"
        else:
            return f"{self.sum}{hit_or_miss} {self.rolls}"
