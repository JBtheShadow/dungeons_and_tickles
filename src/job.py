from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class JobId(Enum):
    WARRIOR = auto()
    WIZARD = auto()
    ROGUE = auto()
    PALADIN = auto()
    PRIEST = auto()
    SCAVENGER = auto()
    LIBRARIAN = auto()
    LICH = auto()
    PROSPECTOR = auto()
    CRAFTSMAN = auto()
    LEE = auto()
    GUARD = auto()
    CULTIST = auto()
    BARBARIAN = auto()
    SPIRITER = auto()
    BEASTMASTER = auto()
    ALCHEMIST = auto()
    GAMBLER = auto()


@dataclass
class Job:
    name: str
    description: str
    st: int = 0
    mp: int = 0
    at: int = 0
    ep: int = 0
    gold: int = 0
    alignment: str = None
    faith: int = 0

    def __post_init__(self):
        self.st += 100
        self.mp += 50
        self.at += 1
        self.ep += 1
        self.gold += 50


JOBS = {
    JobId.WARRIOR: Job(
        'Warrior',
        'Made for combat\n'
        'Naturally grows stronger each round',
        at=2, st=15),
    JobId.WIZARD: Job(
        'Wizard',
        'Made for casting spells\n'
        'Learn new spells each round',
        mp=20),
    JobId.ROGUE: Job(
        'Rogue',
        'Steal for profit\n'
        'Shopkeepers hate them'),
    JobId.PALADIN: Job(
        'Paladin',
        'Upholder of the law and bane of the undead',
        ep=2, st=25),
    JobId.PRIEST: Job(
        'Priest',
        'Made for healing\n'
        'Helping others earns rewards',
        alignment='good', faith=3),
    JobId.SCAVENGER: Job(
        'Scavenger',
        'Find items and coin in the wild\n'
        'Some shopkeepers hate them'),
    JobId.LIBRARIAN: Job('Librarian', 'Bookworm', mp=30),
    JobId.LICH: Job(
        'Lich',
        'Summoner of minions\n'
        'Suffers no penalty upon fainting',
        alignment='evil'),
    JobId.PROSPECTOR: Job('Prospector', 'Made for mining'),
    JobId.PROSPECTOR: Job(
        'Craftsman',
        'Can craft their own items\n'
        'Some shopkeepers hate them'),
    JobId.LEE: Job('Lee', 'Pacifist, wins battles by surviving long enough'),
    JobId.GUARD: Job(
        'Guard',
        'Member of the guild\n'
        'Better and cheaper skills'),
    JobId.CULTIST: Job(
        'Tickle Cultist',
        'Mess with your opponents!\n'
        'Players can opt to become a Tickle Cultist at any point\n'
        'at the cost of losing access to everything from previous class',
        mp=10, alignment='evil'),
    JobId.BARBARIAN: Job(
        'Barbarian',
        'Rage is your only friend\n'
        'Unable to use ranged weapons or cast spells',
        st=30, at=3),
    JobId.SPIRITER: Job(
        'Spiriter',
        'Use the power of spirits to change your fate\n'
        'Or your oponents\'!'),
    JobId.BEASTMASTER: Job(
        'Beastmaster',
        'Tame defeated beasts to enlist them into your cause'),
    JobId.ALCHEMIST: Job(
        'Alchemist',
        'Craft better potions\n'
        'Shopkeepers hate them',
        mp=10),
    JobId.GAMBLER: Job('Gambler', 'Risk taker, double or nothing'),
}
