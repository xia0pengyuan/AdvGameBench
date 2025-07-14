rule = """
1. Turn-based battle between Invaders (Fire, Water, Dark) and Defenders (Wood, Earth, Light). Each side has three characters acting 
in the listed order: Invaders first, then Defenders, then repeat.
2. Each character has three skills. On their turn, they may freely choose any skill — no fixed cycle, and the same skill can be used repeatedly.
3. Elemental chart:
   • Fire > Wood, Wood > Earth, Earth > Water, Water > Fire (×1.2 damage when effective, ×0.8 when resisted)
   • Light ↔ Dark counter (×1.5)
   • All other matchups deal ×1.0
4. A side wins when all opposing characters are eliminated.
"""

invader = """
Fire skills:
- Flame Splash: 12 dmg + 1 Burning layer (5 dmg/round) for 2 rounds. Cost 1
- Residual Warmth: +30% next fire skill for 1 round. Cost 1
- Burst Flame Bomb: 25 base dmg + 4 per Burning layer. Cost 2
- Flame Whirlwind: 5 Burning layers (5 dmg/round) for 3 rounds. Cost 3
- Magma Eruption: 50 base dmg + 8 per Burning layer; clears all Burning layers. Cost 4
- Hell Curtain: 45 dmg + shield that reflects 50 melee dmg for 3 rounds. Cost 5

Water skills:
- Stream Pierce: 10 dmg + 1 permanent Tidal Surge layer. Cost 1
- Water Barrier: 5‑point shield for 3 rounds + 1 Tidal Surge layer. Cost 1
- Whirlpool Strangle: 20 base dmg + 6 per Tidal Surge layer. Cost 2
- Ice Branded: 20 dmg & target takes +60% dmg next turn. Cost 3
- Tsunami Ending: 40 base dmg + 8 per Tidal Surge layer; clears all Tidal Surge layers. Cost 4
- Abyss Resonance: 5 dmg per Tidal Surge layer + shield worth 10 per layer for 4 rounds. Cost 5

Dark skills:
- Shadow Claw: 14 dmg & heal 30% of dmg dealt. Cost 1
- Fear Whisper: −10% dmg taken for 3 rounds. Cost 1
- Soul Siphon: 30 dmg (+25 if target <50% HP). Cost 2
- Night Ambush: 25 dmg & target takes +25% dmg next turn. Cost 3
- Final Announcement: 55 base dmg + 8 per 10% HP lost. Cost 4
- Void Assimilation: Sacrifice 25% current HP to deal true dmg = 250% of HP consumed. Cost 5
"""

defender = """
Wood skills:
- Bud Healing: Heal 7 HP/round for 3 rounds. Cost 1
- Parasitic Seed: 10 dmg now + target takes 5 counter dmg when attacking (3 rounds). Cost 1
- Life Totem: Heal 30 HP + +15% healing received for 3 rounds. Cost 2
- Natural Purification: Remove all debuffs + deal 40 dmg. Cost 3
- Forest Reincarnation: Heal 80 HP; excess → 60% shield for 3 rounds + deal 30 dmg. Cost 4
- Poison Vine: 35 dmg/round for 4 rounds. Cost 5

Earth skills:
- Rock Armor: 12 shield for 3 rounds + reflect 8 melee dmg. Cost 1
- Earth Shock: 20 dmg. Cost 1
- Granite Barrier: −45% dmg taken for 3 rounds. Cost 2
- Quicksand Trap: Delay next 4 incoming dmg by 25% and deal 15 back each trigger (3 rounds). Cost 3
- Earth Pulse: Shield = 10 per 10% HP lost; also deal 10 dmg per layer (permanent). Cost 4
- Core Rebound: Deal 120% of stored dmg; clears store. Cost 5

Light skills:
- Holy Glimmer: Remove one debuff + heal 9 HP + deal 9 dmg. Cost 1
- Faith Emblem: Next dmg taken −20% and converted to healing; reflects 10 dmg once. Cost 1
- Divine Link: Reflect next instance of dmg back to attacker. Cost 2
- Luminous Dispel: Remove one buff + −20% attack for 2 rounds. Cost 3
- Angelic Sanctuary: −40 incoming dmg (flat) for 3 rounds. Cost 4
- Divine Sword: 35 dmg + +30% next skill dmg. Cost 5
"""



