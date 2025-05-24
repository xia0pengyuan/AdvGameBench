from collections import deque
from models import Character, Skill
from battle import battle


def create_team(data, team_name="Team"):
    fighters_data = data.get("invaders") or data.get("defenders")

    team = []
    for i, fighter_info in enumerate(fighters_data):
        element = fighter_info["element"]
        skills = fighter_info["skills"]
        fighter = Character(
            name=f"{team_name}_{element}_{i+1}",
            element=element,
            skills=skills
        )
        team.append(fighter)
    return team


def team_battle(invaders, defenders):
    queue_invaders = deque(invaders)
    queue_defenders = deque(defenders)
    round_num = 1

    while queue_invaders and queue_defenders:
        fighter1 = queue_invaders.popleft()
        fighter2 = queue_defenders.popleft()
        
        winner = battle(fighter1, fighter2)
        
        if winner == fighter1:
            queue_invaders.appendleft(winner)
        else:
            queue_defenders.appendleft(winner)
        
        round_num += 1
        if round_num > 100:
            break

    if queue_invaders:
        winning_team_name = "Invaders"
        remaining_queue = queue_invaders
    else:
        winning_team_name = "Defenders"
        remaining_queue = queue_defenders

    remaining_count = len(remaining_queue)
    remaining_hp_list = [fighter.hp for fighter in remaining_queue]
    
    print(f"{winning_team_name} win!")
