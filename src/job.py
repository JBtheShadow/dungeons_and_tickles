from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class JobID(Enum):
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
    JobID.WARRIOR: Job(
        "Warrior",
        "Made for combat\n" "Naturally grows stronger each round",
        at=2,
        st=15,
    ),
    JobID.WIZARD: Job(
        "Wizard", "Made for casting spells\n" "Learn new spells each round", mp=20
    ),
    JobID.ROGUE: Job("Rogue", "Steal for profit\n" "Shopkeepers hate them"),
    JobID.PALADIN: Job(
        "Paladin", "Upholder of the law and bane of the undead", ep=2, st=25
    ),
    JobID.PRIEST: Job(
        "Priest",
        "Made for healing\n" "Helping others earns rewards",
        alignment="good",
        faith=3,
    ),
    JobID.SCAVENGER: Job(
        "Scavenger", "Find items and coin in the wild\n" "Some shopkeepers hate them"
    ),
    JobID.LIBRARIAN: Job("Librarian", "Bookworm", mp=30),
    JobID.LICH: Job(
        "Lich",
        "Summoner of minions\n" "Suffers no penalty upon fainting",
        alignment="evil",
    ),
    JobID.PROSPECTOR: Job("Prospector", "Made for mining"),
    JobID.PROSPECTOR: Job(
        "Craftsman", "Can craft their own items\n" "Some shopkeepers hate them"
    ),
    JobID.LEE: Job("Lee", "Pacifist, wins battles by surviving long enough"),
    JobID.GUARD: Job("Guard", "Member of the guild\n" "Better and cheaper skills"),
    JobID.CULTIST: Job(
        "Tickle Cultist",
        "Mess with your opponents!\n"
        "Players can opt to become a Tickle Cultist at any point\n"
        "at the cost of losing access to everything from previous class",
        mp=10,
        alignment="evil",
    ),
    JobID.BARBARIAN: Job(
        "Barbarian",
        "Rage is your only friend\n" "Unable to use ranged weapons or cast spells",
        st=30,
        at=3,
    ),
    JobID.SPIRITER: Job(
        "Spiriter",
        "Use the power of spirits to change your fate\n" "Or your oponents'!",
    ),
    JobID.BEASTMASTER: Job(
        "Beastmaster", "Tame defeated beasts to enlist them into your cause"
    ),
    JobID.ALCHEMIST: Job(
        "Alchemist", "Craft better potions\n" "Shopkeepers hate them", mp=10
    ),
    JobID.GAMBLER: Job("Gambler", "Risk taker, double or nothing"),
}
