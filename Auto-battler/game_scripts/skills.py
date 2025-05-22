from status import Status

def type_effectiveness(attacking_element, defending_element):
    if attacking_element == "Fire":
        if defending_element == "Wood":
            return 1.2
        elif defending_element == "Earth":
            return 0.8
    elif attacking_element == "Wood":
        if defending_element == "Water":
            return 1.2
        elif defending_element == "Fire":
            return 0.8
    elif attacking_element == "Water":
        if defending_element == "Earth":
            return 1.2
        elif defending_element == "Wood":
            return 0.8
    elif attacking_element == "Earth":
        if defending_element == "Water":
            return 0.8
        elif defending_element == "Fire":
            return 1.2
    elif attacking_element == "Light":
        if defending_element == "Dark":
            return 1.5
    elif attacking_element == "Dark":
        if defending_element == "Light":
            return 1.5
    return 1.0

def calculate_damage(attacker, defender, skill_power):

    base_damage = skill_power
    if base_damage < 0:
        base_damage = 0

    multiplier = type_effectiveness(attacker.element, defender.element)
    damage = int(base_damage * multiplier)

    # 正确迭代 defender.statuses 中的所有状态对象，累计减伤
    total_damage_reduction = sum(
        s.get_damage_reduction() + s.get_flat_damage_reduction() 
        for status_list in defender.statuses.values() 
        for s in status_list
    )

    final_damage = damage - total_damage_reduction
    if final_damage < 1:
        final_damage = 1
    return final_damage


def flame_splash(attacker, defender):
    damage = 12
    defender.hp -= calculate_damage(attacker, defender, damage)
    # 持续伤害(debuff)：Burning
    burning = Status("Burning", duration=2, layers=1, damage_per_round=5)
    defender.add_status(burning)

def residual_warmth(attacker, defender):
    buff = Status("Residual Warmth", duration=1, layers=1, multiplier=0.3)
    attacker.add_status(buff)

def burst_flame_bomb(attacker, defender):
    base = 25
    extra = defender.get_status_layers("Burning") * 4
    total = base + extra
    defender.hp -= calculate_damage(attacker, defender, total)

def flame_whirlwind(attacker, defender):
    # 5 layers, 5 dmg/round, 持续3轮
    burning = Status("Burning", duration=3, layers=5, damage_per_round=5)
    defender.add_status(burning)

def magma_eruption(attacker, defender):
    base = 50
    extra = defender.get_status_layers("Burning") * 8
    total = base + extra
    defender.hp -= calculate_damage(attacker, defender, total)
    defender.remove_status("Burning")

def hell_curtain(attacker, defender):
    damage = 45
    defender.hp -= calculate_damage(attacker, defender, damage)
    # 反射护盾：反射50点近战伤害，持续3轮
    reflect_amount = 50
    reflect_damage = calculate_damage(attacker, defender, reflect_amount)
    shield = Status("Reflective Shield", duration=3, layers=1, reflect_damage=reflect_damage)
    attacker.add_status(shield)

def stream_pierce(attacker, defender):
    damage = 10
    defender.hp -= calculate_damage(attacker, defender, damage)
    surge = Status("Tidal Surge", duration=999, layers=1)
    attacker.add_status(surge)

def water_barrier(attacker, defender):
    shield = Status("Shield", duration=3, layers=1, shield_value=5)
    attacker.add_status(shield)

def whirlpool_strangle(attacker, defender):
    base = 20
    extra = attacker.get_status_layers("Tidal Surge") * 6
    total = base + extra
    defender.hp -= calculate_damage(attacker, defender, total)

def ice_branded(attacker, defender):
    damage = 20
    defender.hp -= calculate_damage(attacker, defender, damage)
    debuff = Status("Ice Branded", duration=1, layers=1, extra_damage_pct=0.6)
    defender.add_status(debuff)

def tsunami_ending(attacker, defender):
    base = 40
    extra = attacker.get_status_layers("Tidal Surge") * 8
    total = base + extra
    defender.hp -= calculate_damage(attacker, defender, total)
    attacker.remove_status("Tidal Surge")

def abyss_resonance(attacker, defender):
    layers = attacker.get_status_layers("Tidal Surge")
    damage = layers * 5
    defender.hp -= calculate_damage(attacker, defender, damage)
    shield_value = layers * 10
    shield = Status("Shield", duration=4, layers=1, shield_value=shield_value)
    attacker.add_status(shield)

def shadow_claw(attacker, defender):
    damage = 14
    defender.hp -= calculate_damage(attacker, defender, damage)
    heal = int(damage * 0.3)
    attacker.hp += heal

def fear_whisper(attacker, defender):
    debuff = Status("Fear Whisper", duration=3, layers=1, damage_reduction=0.1)
    defender.add_status(debuff)

def soul_siphon(attacker, defender):
    damage = 30
    if defender.hp < defender.max_hp * 0.5:
        damage += 25
    defender.hp -= calculate_damage(attacker, defender, damage)

def night_ambush(attacker, defender):
    damage = 25
    defender.hp -= calculate_damage(attacker, defender, damage)
    debuff = Status("Night Ambush", duration=1, layers=1, extra_damage_pct=0.25)
    defender.add_status(debuff)

def final_announcement(attacker, defender):
    base = 55
    hp_lost_pct = (defender.max_hp - defender.hp) / defender.max_hp
    extra = int((hp_lost_pct // 0.1) * 8)
    total = base + extra
    defender.hp -= calculate_damage(attacker, defender, total)

def void_assimilation(attacker, defender):
    # 牺牲25%当前生命造成250%真实伤害
    sacrifice = int(attacker.hp * 0.25)
    attacker.hp -= sacrifice
    damage = int(sacrifice * 2.5)
    defender.hp -= calculate_damage(attacker, defender, damage)



def bud_healing(attacker, defender):
    hot = Status("Bud Healing", duration=3, layers=1, heal_per_round=7)
    attacker.add_status(hot)

def parasitic_seed(attacker, defender):
    defender.hp -= calculate_damage(attacker, defender, 10)
    counter_damage = calculate_damage(attacker, defender, 5)
    debuff = Status("Parasitic Seed", duration=3, layers=1, counter_damage=counter_damage)
    defender.add_status(debuff)

def life_totem(attacker, defender):
    attacker.hp += 30
    if attacker.hp > attacker.max_hp:
        attacker.hp = attacker.max_hp
    buff = Status("Life Totem", duration=3, layers=1, healing_bonus=0.15)
    attacker.add_status(buff)

def natural_purification(attacker, defender):
    # remove all debuffs from self
    debuffs = ["Fear Whisper", "Ice Branded", "Night Ambush", "Parasitic Seed", "Poison Vine", "Quicksand Trap"]
    for d in debuffs:
        if d in attacker.statuses:
            attacker.remove_status(d)
    defender.hp -= calculate_damage(attacker, defender, 40)

def forest_reincarnation(attacker, defender):
    heal_amount = 80
    new_hp = attacker.hp + heal_amount
    if new_hp > attacker.max_hp:
        excess = new_hp - attacker.max_hp
        attacker.hp = attacker.max_hp
        shield_value = int(excess * 0.6)
        shield = Status("Forest Shield", duration=3, layers=1, shield_value=shield_value)
        attacker.add_status(shield)
    else:
        attacker.hp = new_hp
    defender.hp -= calculate_damage(attacker, defender, 30)

def poison_vine(attacker, defender):
    damage_per_round = calculate_damage(attacker, defender, 35)
    debuff = Status("Poison Vine", duration=4, layers=1, damage_per_round=damage_per_round)
    defender.add_status(debuff)

# Earth Skills

def rock_armor(attacker, defender):
    shield = Status("Rock Armor", duration=3, layers=1, shield_value=12, reflect_damage=calculate_damage(attacker, defender, 8))
    attacker.add_status(shield)

def earth_shock(attacker, defender):
    defender.hp -= calculate_damage(attacker, defender, 20)

def granite_barrier(attacker, defender):
    buff = Status("Granite Barrier", duration=3, layers=1, damage_reduction=0.45)
    attacker.add_status(buff)

def quicksand_trap(attacker, defender):
    trap_damage = calculate_damage(attacker, defender, 15)
    debuff = Status("Quicksand Trap", duration=3, layers=1,
                   delay_damage=0.25, delay_triggers=4, trap_damage=trap_damage)
    defender.add_status(debuff)

def earth_pulse(attacker, defender):
    hp_lost_pct = (attacker.max_hp - attacker.hp) / attacker.max_hp
    layers = int(hp_lost_pct / 0.1)
    shield_value = layers * 10
    shield = Status("Earth Pulse Shield", duration=999, layers=1, shield_value=shield_value)
    attacker.add_status(shield)
    # also deal 10 dmg per layer to defender
    if layers > 0:
        defender.hp -= calculate_damage(attacker, defender, layers * 10)

def core_rebound(attacker, defender):
    stored = getattr(attacker, "stored_damage", 0)
    rebound = int(stored * 1.2)
    if rebound > 0:
        defender.hp -= calculate_damage(attacker, defender, rebound)
    attacker.stored_damage = 0

# Light Skills

def holy_glimmer(attacker, defender):
    # remove one debuff from self
    for d in ["Fear Whisper", "Ice Branded", "Night Ambush", "Parasitic Seed", "Poison Vine", "Quicksand Trap"]:
        if d in attacker.statuses:
            attacker.remove_status(d)
            break
    attacker.hp += 9
    if attacker.hp > attacker.max_hp:
        attacker.hp = attacker.max_hp
    defender.hp -= calculate_damage(attacker, defender, 9)

def faith_emblem(attacker, defender):
    buff = Status("Faith Emblem", duration=1, layers=1,
                  damage_reduction=0.2, convert_to_healing=True, retaliation_damage=10)
    attacker.add_status(buff)

def divine_link(attacker, defender):
    buff = Status("Divine Link", duration=1, layers=1, reflect_next=True)
    attacker.add_status(buff)

def luminous_dispel(attacker, defender):
    # remove one buff from defender
    for b in ["Life Totem", "Granite Barrier", "Faith Emblem", "Earth Pulse Shield", "Rock Armor"]:
        if b in defender.statuses:
            defender.remove_status(b)
            break
    debuff = Status("Luminous Dispel", duration=2, layers=1, damage_reduction=0.2)
    defender.add_status(debuff)

def angelic_sanctuary(attacker, defender):
    buff = Status("Angelic Sanctuary", duration=3, layers=1, flat_damage_reduction=40)
    attacker.add_status(buff)

def divine_sword(attacker, defender):
    # deal 30 dmg
    defender.hp -= calculate_damage(attacker, defender, 35)
    # give +30% next skill damage
    buff = Status("Divine Sword Buff", duration=1, layers=1, multiplier=0.3)
    attacker.add_status(buff)

