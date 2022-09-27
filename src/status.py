from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class StatusID(Enum):
    # Regular status effects
    LGI = auto()
    TS = auto()
    REGEN = auto()
    LRA = auto()
    EVADE = auto()
    BLIND = auto()
    WEAKEN = auto()
    WEAKEN_ENEMY = auto()
    STRENGTHEN = auto()

    # Peacock curses and blessings
    CURSE_LEETHALITY = auto()
    BLESSING_LIFE = auto()
    BLESSING_MAGIC = auto()
    BLESSING_STRENGTH = auto()
    BLESSING_STRENGTH_LEE = auto()
    CURSE_SENSITIVITY = auto()
    BLESSING_ENDURANCE = auto()
    BLESSING_EVASION = auto()
    BLESSING_RICHES = auto()
    CURSE_FEATHER = auto()


class StatusType(Enum):
    INSTANT = auto()
    INSTANT_IN_BATTLE = auto()
    WHOLE_BATTLE = auto()
    WHOLE_ROUND = auto()
    FADES_OVER_TIME_IN_BATTLE = auto()
    FADES_ON_USE = auto()


@dataclass
class StatusInfo:
    status_id: StatusID
    name: str
    long_name: str = None
    description: str = None
    status_type: StatusType = None
    peacock: bool = False
    blessing: bool = False
    curse: bool = False
    conditional: bool = False

    def __post_init__(self):
        if not self.long_name:
            self.long_name = self.name

    @staticmethod
    def from_id(status_id: StatusID):
        return _STATUS[status_id]


_STATUS = {
    # Regular status effects
    StatusID.LGI: StatusInfo(
        status_id=StatusID.LGI,
        name="LGI",
        long_name="Laughing Gas Intoxication",
        description="Take X damage each battle turn, ends after battle",
        status_type=StatusType.WHOLE_BATTLE,
    ),
    StatusID.TS: StatusInfo(
        status_id=StatusID.TS,
        name="TS",
        long_name="Ticklish Sensations",
        description="Take X damage each battle turn, prevents healing, "
        "slowly fades away as the battle progresses",
        status_type=StatusType.FADES_OVER_TIME_IN_BATTLE,
    ),
    StatusID.REGEN: StatusInfo(
        status_id=StatusID.REGEN,
        name="Regeneration",
        description="Heal X ST each battle turn, slowly fades away as "
        "the battle progresses",
        status_type=StatusType.FADES_OVER_TIME_IN_BATTLE,
    ),
    StatusID.LRA: StatusInfo(
        status_id=StatusID.LRA,
        name="LRA",
        long_name="Laugh Resist Aura",
        description="Protects from X amount of damage once, fades upon being hit",
        status_type=StatusType.FADES_ON_USE,
    ),
    StatusID.EVADE: StatusInfo(
        status_id=StatusID.EVADE,
        name="Evade",
        description="Dodges a single attack, forcing it to miss. Fades afterwards",
        status_type=StatusType.FADES_ON_USE,
    ),
    StatusID.BLIND: StatusInfo(
        status_id=StatusID.BLIND,
        name="Blind",
        description="Guarantees your next attack will miss. Still triggers Evade. "
        "Fades afterwards",
        status_type=StatusType.FADES_ON_USE,
    ),
    StatusID.WEAKEN: StatusInfo(
        status_id=StatusID.WEAKEN,
        name="Weaken",
        description="Deals X less damage and -X modifier to all rolls. "
        "Fades over time",
        status_type=StatusType.FADES_OVER_TIME_IN_BATTLE,
    ),
    StatusID.WEAKEN_ENEMY: StatusInfo(
        status_id=StatusID.WEAKEN_ENEMY,
        name="Weaken",
        description="Deals 5X less damage and -X modifier to all rolls. "
        "Fades over time",
        status_type=StatusType.FADES_OVER_TIME_IN_BATTLE,
        conditional=True,
    ),
    StatusID.STRENGTHEN: StatusInfo(
        status_id=StatusID.STRENGTHEN,
        name="Strengthen",
        description="Deals X more damage and +X modifier to all rolls. "
        "Fades over time",
        status_type=StatusType.FADES_OVER_TIME_IN_BATTLE,
    ),
    # Curses and blessings
    StatusID.CURSE_LEETHALITY: StatusInfo(
        status_id=StatusID.CURSE_LEETHALITY,
        name="Curse of Leethality",
        description="On your next fight you will feel more sensitive than "
        "normal, taking +5 damage each hit for the entire battle",
        status_type=StatusType.WHOLE_BATTLE,
        peacock=True,
        curse=True,
    ),
    StatusID.BLESSING_LIFE: StatusInfo(
        status_id=StatusID.BLESSING_LIFE,
        name="Blessing of Life",
        description="You restore 50 ST and gain 25 max ST",
        status_type=StatusType.INSTANT,
        peacock=True,
        blessing=True,
    ),
    StatusID.BLESSING_MAGIC: StatusInfo(
        status_id=StatusID.BLESSING_MAGIC,
        name="Blessing of Magic",
        description="You restore 30 MP and gain 15 max MP",
        status_type=StatusType.INSTANT,
        peacock=True,
        blessing=True,
    ),
    StatusID.BLESSING_STRENGTH: StatusInfo(
        status_id=StatusID.BLESSING_STRENGTH,
        name="Blessing of Strength",
        description="You increase your AT by 2 and get Strengthen(5) this turn",
        status_type=StatusType.INSTANT,
        peacock=True,
        blessing=True,
    ),
    StatusID.BLESSING_STRENGTH_LEE: StatusInfo(
        status_id=StatusID.BLESSING_STRENGTH_LEE,
        name="Blessing of Strength",
        description="The next enemy you fight is inflicted with Weaken(2)",
        status_type=StatusType.INSTANT_IN_BATTLE,
        peacock=True,
        blessing=True,
        conditional=True,
    ),
    StatusID.CURSE_SENSITIVITY: StatusInfo(
        status_id=StatusID.CURSE_SENSITIVITY,
        name="Curse of Sensitivity",
        description="On your next fight your EP is set to 0 and you can only "
        "increase it with skills or spells during this turn",
        status_type=StatusType.WHOLE_BATTLE,
        peacock=True,
        curse=True,
    ),
    StatusID.BLESSING_ENDURANCE: StatusInfo(
        status_id=StatusID.BLESSING_ENDURANCE,
        name="Blessing of Endurance",
        description="You restore 3 EP and gain 1 max EP (up to 10 EP)",
        status_type=StatusType.INSTANT,
        peacock=True,
        blessing=True,
    ),
    StatusID.BLESSING_EVASION: StatusInfo(
        status_id=StatusID.BLESSING_EVASION,
        name="Blessing of Evasion",
        description="You dodge the next two non-crit attacks. "
        "Crits deal regular damage instead",
        status_type=StatusType.FADES_ON_USE,
        peacock=True,
        blessing=True,
    ),
    StatusID.BLESSING_RICHES: StatusInfo(
        status_id=StatusID.BLESSING_RICHES,
        name="Blessing of Riches",
        description="200 gold is summoned in front of you and you receive "
        "double the gold from all sources for the rest of this turn ",
        status_type=StatusType.WHOLE_ROUND,
        peacock=True,
        blessing=True,
    ),
    StatusID.CURSE_FEATHER: StatusInfo(
        status_id=StatusID.CURSE_FEATHER,
        name="Curse of the Feather",
        description="You gain one non-magical feather that you must " "use on yourself",
        status_type=StatusType.INSTANT,
        peacock=True,
        curse=True,
    ),
}


PEACOCK_EFFECTS = {
    status_id
    for status_id, status in _STATUS.items()
    if not status.conditional and status.peacock
}
