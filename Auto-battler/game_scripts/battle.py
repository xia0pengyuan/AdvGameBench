from models import Character, Skill
import skills


def battle(fighter1, fighter2):
    turn = 0
    while fighter1.is_alive() and fighter2.is_alive():
        if turn % 2 == 0:
            attacker, defender = fighter1, fighter2
        else:
            attacker, defender = fighter2, fighter1

        skill = attacker.get_next_skill()

        func_name = skill.lower().replace(" ", "_")
        effect_func = getattr(skills, func_name, None)
        if effect_func:
            Character.attack(attacker, defender, effect_func)
        
        turn += 1

    winner = fighter1 if fighter1.is_alive() else fighter2
    loser = fighter2 if fighter1.is_alive() else fighter1
    return winner