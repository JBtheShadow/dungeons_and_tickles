from __future__ import annotations


class Job:
    def __init__(self,
                 name: str,
                 description: str | list[str],
                 bonus_st: int = 0,
                 bonus_mp: int = 0,
                 bonus_at: int = 0,
                 bonus_ep: int = 0,
                 alignment: str = None,
                 bonus_faith: int = 0):
        self.name = name
        self.description = description
        self.st = 100 + bonus_st
        self.mp = 50 + bonus_mp
        self.at = 1 + bonus_at
        self.ep = 1 + bonus_ep
        self.gold = 50
        self.alignment = alignment
        self.faith = bonus_faith


JOBS = {
    'warrior': Job('Warrior', [
        'Made for combat',
        'Naturally grows stronger each round',
    ], bonus_at=2, bonus_st=15),
    'wizard': Job('Wizard', [
        'Made for casting spells',
        'Learn new spells each round',
    ], bonus_mp=20),
    'rogue': Job('Rogue', [
        'Steal for profit',
        'Shopkeepers hate them',
    ]),
    'paladin': Job('Paladin', 'Upholder of the law and bane of the undead',
                   bonus_ep=2, bonus_st=25),
    'priest': Job('Priest', [
        'Made for healing',
        'Helping others earns rewards'
    ], alignment='good', bonus_faith=3),
    'scavenger': Job('Scavenger', [
        'Find items and coin in the wild',
        'Some shopkeepers hate them',
    ]),
    'librarian': Job('Librarian', 'Bookworm', bonus_mp=30),
    'lich': Job('Lich', [
        'Summoner of minions',
        'Suffers no penalty upon fainting',
    ], alignment='evil'),
    'prospector': Job('Prospector', 'Made for mining'),
    'craftsman': Job('Craftsman', [
        'Can craft their own items',
        'Some shopkeepers hate them',
    ]),
    'lee': Job('Lee', 'Pacifist, wins battles by surviving long enough'),
    'guard': Job('Guard', [
        'Member of the guild',
        'Better and cheaper skills'
    ]),
    'cultist': Job('Tickle Cultist', [
        'Mess with your opponents!',
        'Players can opt to become a Tickle Cultist at any point',
        'at the cost of losing access to everything from previous class'
    ], bonus_mp=10, alignment='evil'),
    'barbarian': Job('Barbarian', [
        'Rage is your only friend',
        'Unable to use ranged weapons or cast spells'
    ], bonus_st=30, bonus_at=3),
    'spiriter': Job('Spiriter', [
        'Use the power of spirits to change your fate',
        'Or your oponents\'!'
    ]),
    'beastmaster': Job('Beastmaster',
                       'Tame defeated beasts to enlist them into your cause'),
    'alchemist': Job('Alchemist', [
        'Craft better potions',
        'Shopkeepers hate them'
    ], bonus_mp=10),
    'gambler': Job('Gambler', 'Risk taker, double or nothing'),
}
