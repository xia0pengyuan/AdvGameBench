human = """HandgunSoldier: health: 3, shooting interval: 1000ms, cost: 100, damage per shot: 1, no special abilities.
RifleSoldier: health: 3, shooting interval: 500ms, cost: 200, damage per shot: 1, no special abilities.
MachineGunSoldier: health: 3, shooting interval: 250ms, cost: 400, damage per shot: 1, no special abilities.
ShieldSoldier: health: 15, cost: 50, only for defense, no attack capabilities.
EnhancedShieldSoldier: health: 30, cost: 100, only for defense, no attack capabilities and Bouncing Demon cannot jump over.
FlamethrowerSoldier: health: 2, cost: 200, shooting interval: 1000ms, damage per shot: 1, deals an additional 1 damage every 1000ms.
IceSoldier: health: 2, shooting interval: 1000ms, cost: 200, damage per shot: 1, reduces enemy speed by half.
AntiAirSoldier: health: 2, shooting interval: 1000ms, cost: 100, damage per shot: 1, can only attack airborne units.
Bomb: health: 50, detonation time: 500ms, cost: 200, explosion range: 3×3, damage per explosion: 30, destroyed after detonation.
LinearExplosion: health: 50, detonation time: 500ms, cost: 200,  explosion range: the entire row, damage per explosion: 30, destroyed after detonation.
MagneticSoldier: health: 2, shooting interval: 2000ms, cost: 100, damage per shot: 0, releases a magnetic pulse that disables the defensive abilities of ShieldDemon and MachineDemon.
"""

demon = """A speed of 2 requires 14 seconds to travel from spawn to the last human grid.
NormalDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 100, damage per attack: 1, no special abilities.
GreatDemon: health: 20, speed: 2, attack interval: 1000ms, cost: 200, damage per attack: 1, higher health.
DemonKing: health: 40, speed: 2, attack interval: 1000ms, cost: 400, damage per attack: 5.
SpeedyDemon: health: 10, speed: 4, attack interval: 1000ms, cost: 150, damage per attack: 1, moves faster.
ShieldDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 200, damage per attack: 1, takes 70% less damage from normal attacks.
MachineDemon: health: 20, speed: 2 (increases to 3 when activated), attack interval: 1000ms, cost: 300, damage per attack: 3, reduced damage due to mechanical body.
BouncingDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 150, damage per attack: 1, can jump over certain units except for the EnhancedShieldSoldier.
ShieldBreakerDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 150, damage per attack: 1 (×5 against shield units).
FrostDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 150, damage per attack: 1, immune to ice damage and unaffected by slow effects.
FlyingDemon: health: 10, speed: 2, attack interval: 1000ms, cost: 200, damage per attack: 1, can only be attacked by AntiAirSoldier.
"""

rule = """1.Players can purchase characters and place them on the battlefield. The battlefield consists of 5 rows (corresponding to y-coordinates 0-4). The human side can place units in a designated area spanning 11 columns (corresponding to x-coordinates 0-10).
2.Demon spawn from the right side of the battlefield (x-coordinates 11) and move left. Human units are placed on the left side of the battlefield, remain stationary, and attack approaching enemies.
3. All units attack according to their attack interval, automatically attacking when their cooldown ends. defending units fire bullets or activate skills to attack enemies. invaders units engage in melee attacks when they come into contact with defending units.
4. Each grid cell can only contain one human unit at a time. Placing a new unit in an occupied cell is not allowed.
5. When an attack hits, the target takes damage based on the attacker's power. If a unit's health drops to 0, it is eliminated and removed from the battlefield.
6. If all demons are eliminated, the human wins. If any demons successfully reaches the left side of the battlefield, the human loses.
"""
