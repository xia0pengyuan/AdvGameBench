rule ="""1.At the start of the game, players can purchase all desired characters at once, up to a maximum of 7 characters. Gold characters cost three times as much as bronze characters, 
but their stats (attack, health, numerical skill effects, etc.) are twice as high. Non-numerical skills are not affected by this multiplier.
2.Initiative Determination: The side with more characters attacks first. If both sides have the same number of characters, the invader attacks first.
3.Elemental Advantage: Certain elements have an advantage over others, granting a bonus in combat (Fire > Nature, Nature > Water, Water > Earth, Earth > Fire).
4.Battle Process: Both sides will attack based on their respective target_priority (target priority). However, if there are Taunt minions on the opponent's side, attackers must prioritize attacking them.
The attack order follows a left-to-right sequence. The first minion in the invaders or defenders list (as defined in the JSON file) will attack first, depending on which side has the initiative. 
After that, the first minion from the opposing side attacks. Then, the second minion from the attacking side follows, then the second minion from the opposing side, and so on in an alternating pattern.
If a minion's health reaches zero, it is eliminated. The battle continues with both sides attacking in turns until one side is completely wiped out, resulting in victory for the other side.
5.If all characters on one side are eliminated, the other side wins.
6.If both sides are eliminated simultaneously in the same attack resolution, the Invader wins."""

invader_information = """FireLizard: Attack: 2, Health: 2, Cost: 1, Ability: Deals 2 damage to the enemy that killed it upon death.
WaterElemental: Attack: 2, Health: 2, Cost: 1, Ability: Gains +1 Attack when attacking.
PoisonFrog: Attack: 1, Health: 1, Cost: 2, Ability: Instantly destroys any minion it damages.
MoltenHound: Attack: 3, Health: 1, Cost: 2, Ability: Deals 1 damage to all enemies upon death.
BattleFrenzy: Attack: 7, Health: 4, Cost: 2, Ability: Each attack reduces its Attack by 4.
BanditLeader: Attack: 8, Health: 3, Cost: 3, Ability: Any excess damage from an attack carries over to the next target.
LavaGolem: Attack: 1, Health: 8, Cost: 3, Ability: Forces enemies to attack this minion first, Burns the attacker for 3 damage per turn when hit.
TideGuardian: Attack: 4, Health: 2, Cost: 3, Ability: Absorbs the first source of damage taken (divine shield), Attacks twice each turn.
TideLord: Attack: 4, Health: 9, Cost: 5, Ability: Doubles its Attack when taking damage.
Phoenix: Attack: 5, Health: 5, Cost: 5, Ability: Deals damage equal to its Attack to the target and its adjacent enemies, Revives with full Health after being defeated once per game.
ShadowOverlord: Attack: 4, Health: 4, Cost: 5, Ability: Summons a Slow Skeleton (3/1) upon death."""

defender_information = """Sapling: Attack: 2, Health: 2, Cost: 1, Ability: Gains +1 Health when attacking.
RockBeetle: Attack: 1, Health: 5, Cost: 1, Ability: Forces enemies to attack this minion before others.
ForestSeer: Attack: 2, Health: 2, Cost: 2, Ability: At the start of the game, grants +1 Attack and +2 Health to all Nature Allies.
StoneWarrior: Attack: 2, Health: 5, Cost: 2, Ability: Forces enemies to attack this minion before others. Summons a RockBeetle upon death.
EliteSoldier: Attack: 1, Health: 1, Cost: 2, Ability: At the start of the game, grants Divine Shield to adjacent minions and +1 Attack.
Paladin: Attack: 3, Health: 6, Cost: 3, Ability: Has Divine Shield; gains +2 Attack whenever a friendly minion loses its Divine Shield.
BlackRock: Attack: 5, Health: 1, Cost: 3, Ability: At the start of the game, gains +3 Health for each friendly minion.
VineProtector: Attack: 5, Health: 4, Cost: 3, Ability: Upon death, restores 2 Health to all friendly minions.
King: Attack: 3, Health: 10, Cost: 5, Ability: Summons a 2/2 Soldier with Divine Shield whenever it attacks (if there is an open space).
MountainGiant: Attack: 4, Health: 9, Cost: 5, Ability: Forces enemies to attack this minion first, Reduces the attack of the attacker by 2 when hit.
AncientTreant: Attack: 4, Health: 4, Cost: 5, Ability: At the start of the game, grants +3 Attack and +3 Health to all allied minions.
"""



