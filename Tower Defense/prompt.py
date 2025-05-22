human = """HandgunSoldier: HP 3, shot every 1000 ms, cost 100, dmg 1
RifleSoldier: HP 3, shot every 500 ms, cost 200, dmg 1
MachineGunSoldier: HP 3, shot every 250 ms, cost 400, dmg 1
ShieldSoldier: HP 15, cost 50, defense only
EnhancedShieldSoldier: HP 30, cost 100, defense only; blocks BouncingDemon
FlamethrowerSoldier: HP 2, shot every 1000 ms, cost 200, dmg 1 + 1 burn/sec
IceSoldier: HP 2, shot every 1000 ms, cost 200, dmg 1, slows enemies × 0.5
AntiAirSoldier: HP 2, shot every 1000 ms, cost 100, dmg 1, air‐only
LinearExplosion: HP 50, detonate in 500 ms, cost 200, range entire row, dmg 30, one‐use
MagneticSoldier: HP 2, shot every 2000 ms, cost 100, dmg 0; emits pulse disabling ShieldDemon & MachineDemon defenses
"""

demon = """Default speed 2 (14 s from spawn to last grid).
NormalDemon: HP 10, cost 100, dmg 1, no special abilities
GreatDemon: HP 20, cost 200, dmg 1
DemonKing: HP 80, cost 800, dmg 5
SpeedyDemon: HP 10, speed 4, cost 150, dmg 1
ShieldDemon: HP 10, cost 200, dmg 1, takes 70 % less normal damage
MachineDemon: HP 20, cost 300, dmg 3, mechanical (reduced damage), speed 3 when activated
BouncingDemon: HP 10, cost 150, dmg 1, can jump over most units (not EnhancedShieldSoldier)
ShieldBreakerDemon: HP 10, cost 150, dmg 1 (×5 vs shielded units)
FireDemon: HP 10, cost 150, dmg 1, immune to fire
FrostDemon: HP 10, cost 150, dmg 1, immune to ice, unaffected by slows
FlyingDemon: HP 10, cost 200, dmg 1, can only be attacked by AntiAirSoldier
SummoningDemon: HP 10, speed 1, cost 400, dmg 1, summons a NormalDemon adjacent every 5 s
"""

rule = """1.Players can purchase characters and place them on the battlefield. The battlefield consists of 5 rows (corresponding to y-coordinates 0-4). The human side can place units in a designated area spanning 11 columns (corresponding to x-coordinates 0-10).
2. Demon spawn from the right side of the battlefield (x-coordinates 11) and move left. Human units are placed on the left side of the battlefield, remain stationary, and attack approaching enemies.
3. All units attack according to their attack interval, automatically attacking when their cooldown ends. defending units fire bullets or activate skills to attack enemies. invaders units engage in melee attacks when they come into contact with defending units.
4. Each grid cell can only contain one human unit at a time. Placing a new unit in an occupied cell is not allowed.
5. When an attack hits, the target takes damage based on the attacker's power. If a unit's health drops to 0, it is eliminated and removed from the battlefield.
6. If all demons are eliminated, the human wins. If any demons successfully reaches the left side of the battlefield, the human loses.

Reminder: every unit entry must include a "name" field.  
"""
