rule = """1. Buy up to 7 characters at once; Gold cost triple, Attack/Health and numeric effects double; non‑numeric unaffected; in JSON use property tier with value Gold
2. Initiative goes to side with more characters; tie gives Invader priority
3. Elemental cycle is Fire > Nature > Water > Earth > Fire
4. Battle proceeds with initiative first, alternating left‑to‑right attacks; must target Taunt if present; follow target priority if available, otherwise attack left‑to‑right; remove units at zero HP; repeat until one side is eliminated.
5. Full elimination causes that side to lose; simultaneous elimination gives Invader the win
6. If a character’s 'tier' property is absent, default its tier to "Bronze"."""

invader = """FireLizard (atk2 hp2 cost1) with Deathrattle that deals 2 damage to its killer
WaterElemental (atk2 hp2 cost1) gains +1 Attack when attacking
PoisonFrog (atk1 hp1 cost2) destroys any minion it damages
MoltenHound (atk3 hp1 cost2) with Deathrattle that deals 1 damage to all enemies
BattleFrenzy (atk7 hp4 cost2) loses 4 Attack after each attack
BanditLeader (atk8 hp3 cost3) carries excess damage to the next target
LavaGolem (atk1 hp8 cost3) has Taunt and burns its attacker for 3 damage per turn
TideGuardian (atk4 hp2 cost3) has Divine Shield and attacks twice
TideLord (atk4 hp10 cost4) doubles Attack when damaged
Phoenix (atk5 hp5 cost4) deals splash damage to adjacent units and revives once
ShadowOverlord (atk4 hp4 cost4) summons a 3/1 Skeleton on death"""

defender = """Sapling (atk2 hp2 cost1) gains 1 Health when attacking
RockBeetle (atk1 hp5 cost1) has Taunt
ForestSeer (atk1 hp2 cost2) gives Nature allies 1 Attack and 1 Health at game start
StoneWarrior (atk2 hp5 cost2) has Taunt and summons a RockBeetle on death
EliteSoldier (atk1 hp1 cost2) grants adjacent units Divine Shield and +1 Attack at game start
Paladin (atk3 hp6 cost3) has Divine Shield and gains 2 Attack when a friendly unit loses Divine Shield
BlackRock (atk2 hp1 cost3) gains 3 Health per friendly unit at game start
VineProtector (atk3 hp4 cost3) restores 2 Health to all friendly units on death
King (atk3 hp12 cost4) summons a 1/1 Divine Shield Soldier when attacking if space is open
MountainGiant (atk4 hp9 cost4) has Taunt and reduces an attacker’s Attack by 2 when hit
AncientTreant (atk2 hp3 cost4) grants all allies 2 Attack and 2 Health at game start"""

