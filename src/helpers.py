from __future__ import annotations
from dataclasses import dataclass
from random import randint


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

    def roll_advantage(self):
        rolls = [
            [randint(1, self.sides) for _ in range(2)]
            for _ in range(self.number)
        ]
        rolls_adv = [max(r) for r in rolls]
        return sum(rolls_adv) + self.mod, rolls_adv, rolls
