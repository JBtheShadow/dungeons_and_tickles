from __future__ import annotations

from random import randint


def print_dice(number, sides, mod=0):
    if mod > 0:
        return f"{number}d{sides}+{mod}"
    elif mod < 0:
        return f"{number}d{sides}{mod}"
    else:
        return f"{number}d{sides}"


def dice_roll(number, sides, mod=0):
    rolls = [randint(1, sides) for _ in range(number)]
    return sum(rolls) + mod, rolls


def dice_roll_advantage(number, sides, mod=0):
    rolls = [[randint(1, sides) for _ in range(2)] for _ in range(number)]
    rolls_adv = [max(r) for r in rolls]
    return sum(rolls_adv) + mod, rolls_adv, rolls
