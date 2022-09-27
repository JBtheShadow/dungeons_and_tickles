from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TrapID(Enum):
    # Encounter trap
    DUNGEON_TICKLE_TRAP = auto()

    # Item traps
    TICKLE_TRAP = auto()
    TOLLBOOTH = auto()
    TICKLE_GLUE_TRAP = auto()
    TRIPWIRE = auto()
    STOCKS_TELEPORTER = auto()


@dataclass
class TrapInfo:
    trap_id: TrapID
    name: str
    description: str
    # Remaining attributes temporarily removed
    # for this refactoring phase

    @staticmethod
    def from_id(trap_id: TrapID):
        return _TRAPS[trap_id]


_TRAPS = {
    TrapID.DUNGEON_TICKLE_TRAP: TrapInfo(
        trap_id=TrapID.DUNGEON_TICKLE_TRAP,
        name="Tickle Trap",
        description="Deals 25 ST",
    ),
    TrapID.TICKLE_TRAP: TrapInfo(
        trap_id=TrapID.TICKLE_TRAP,
        name="Tickle Trap",
        description="Deals 5 ST and applies -10 modifier",
    ),
    TrapID.TOLLBOOTH: TrapInfo(
        trap_id=TrapID.TOLLBOOTH,
        name="Tollbooth",
        description="Players pay 25 gold to pass by this\n"
        "Owner of the trap receives amount collected\n"
        "Lasts until player's next turn",
    ),
    TrapID.TICKLE_GLUE_TRAP: TrapInfo(
        trap_id=TrapID.TICKLE_GLUE_TRAP,
        name="Tickle Glue Trap",
        description="Players lose their turn and take 10ST damage from this",
    ),
    TrapID.TRIPWIRE: TrapInfo(
        trap_id=TrapID.TRIPWIRE,
        name="Tripwire",
        description="When triggered if target rolls lower than owner then owner steals "
        "an item and tickles target for 1d6+AT damage",
    ),
    TrapID.STOCKS_TELEPORTER: TrapInfo(
        trap_id=TrapID.STOCKS_TELEPORTER,
        name="Stocks Teleporter",
        description="When a player visits a location roll against the trapper "
        "to check if they see an almost invisible gray pad on the floor which "
        "when stepped on teleports the target to the public stocks\n"
        "Targets on the public stocks have to spend 2 actions to get out and "
        "are dealt 15 ST damage as they're tickled by the town inhabitants. "
        "Lacking actions, they remain stuck until their next turn.\n"
        "Other players are welcome to spend an action and deal 1d6+AT to the "
        "stuck player, while the trapper can do so at no cost.\n"
        "Players in the public stocks may be tickled by anyone without "
        "incurring any faith penalties",
    ),
}
