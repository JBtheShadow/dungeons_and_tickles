from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from passive import PassiveID


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
    TRAPPER = auto()


@dataclass
class Job:
    job_id: JobID
    name: str
    description: str
    st: int = 0
    mp: int = 0
    at: int = 0
    ep: int = 0
    gold: int = 0
    alignment: str = None
    faith: int = 0
    passive_ids: list[PassiveID] = field(default_factory=list)

    def __post_init__(self):
        self.st += 100
        self.mp += 50
        self.at += 1
        self.ep += 1
        self.gold += 50


JOBS = {
    JobID.WARRIOR: Job(
        job_id=JobID.WARRIOR,
        name="Warrior",
        description="Made for combat\n" "Naturally grows stronger each round",
        at=2,
        st=15,
    ),
    JobID.WIZARD: Job(
        job_id=JobID.WIZARD,
        name="Wizard",
        description="Made for casting spells\n" "Learn new spells each round",
        mp=20,
    ),
    JobID.ROGUE: Job(
        job_id=JobID.ROGUE,
        name="Rogue",
        description="Steal for profit\n" "Shopkeepers hate them",
    ),
    JobID.PALADIN: Job(
        job_id=JobID.ROGUE,
        name="Paladin",
        description="Upholder of the law and bane of the undead",
        ep=2,
        st=25,
    ),
    JobID.PRIEST: Job(
        job_id=JobID.PRIEST,
        name="Priest",
        description="Made for healing\n" "Helping others earns rewards",
        alignment="good",
        faith=3,
    ),
    JobID.SCAVENGER: Job(
        job_id=JobID.SCAVENGER,
        name="Scavenger",
        description="Find items and coin in the wild\n" "Some shopkeepers hate them",
    ),
    JobID.LIBRARIAN: Job(
        job_id=JobID.LIBRARIAN, name="Librarian", description="Bookworm", mp=30
    ),
    JobID.LICH: Job(
        job_id=JobID.LICH,
        name="Lich",
        description="Summoner of minions\n" "Suffers no penalty upon fainting",
        alignment="evil",
    ),
    JobID.PROSPECTOR: Job(
        job_id=JobID.PROSPECTOR, name="Prospector", description="Made for mining"
    ),
    JobID.PROSPECTOR: Job(
        job_id=JobID.PROSPECTOR,
        name="Craftsman",
        description="Can craft their own items\n" "Some shopkeepers hate them",
    ),
    JobID.LEE: Job(
        job_id=JobID.LEE,
        name="Lee",
        description="Pacifist, wins battles by surviving long enough",
    ),
    JobID.GUARD: Job(
        job_id=JobID.GUARD,
        name="Guard",
        description="Member of the guild\n" "Better and cheaper skills",
    ),
    JobID.CULTIST: Job(
        job_id=JobID.CULTIST,
        name="Tickle Cultist",
        description="Mess with your opponents!\n"
        "Players can opt to become a Tickle Cultist at any point\n"
        "at the cost of losing access to everything from previous class",
        mp=10,
        alignment="evil",
    ),
    JobID.BARBARIAN: Job(
        job_id=JobID.BARBARIAN,
        name="Barbarian",
        description="Rage is your only friend\n"
        "Unable to use ranged weapons or cast spells",
        st=30,
        at=3,
    ),
    JobID.SPIRITER: Job(
        job_id=JobID.SPIRITER,
        name="Spiriter",
        description="Use the power of spirits to change your fate\n"
        "Or your oponents'!",
    ),
    JobID.BEASTMASTER: Job(
        job_id=JobID.BEASTMASTER,
        name="Beastmaster",
        description="Tame defeated beasts to enlist them into your cause",
    ),
    JobID.ALCHEMIST: Job(
        job_id=JobID.ALCHEMIST,
        name="Alchemist",
        description="Craft better potions\n" "Shopkeepers hate them",
        mp=10,
    ),
    JobID.GAMBLER: Job(
        job_id=JobID.GAMBLER,
        name="Gambler",
        description="Risk taker, double or nothing",
    ),
    JobID.TRAPPER: Job(
        job_id=JobID.TRAPPER,
        name="Trapper",
        description="Expert at trapping others while avoiding getting caught",
    ),
}
