from team import create_team, team_battle
import json
import sys
import os

def main(invader_data, defender_data):

    invaders = create_team(invader_data)
    defenders = create_team(defender_data)

    team_battle(invaders, defenders)

if __name__ == "__main__":

    """
    with open('invader.json', "r", encoding="utf-8") as file:
        invader_data = json.load(file)

    with open('defender.json', "r", encoding="utf-8") as file:
        defender_data = json.load(file)


    main(invader_data, defender_data)


    """
    try:
        if len(sys.argv) < 3:
            print("Usage: python game.py '<human_data_json>' '<demon_data_json>'")
            sys.exit(1)
        
        defender_data = json.loads(sys.argv[1])
        invader_data = json.loads(sys.argv[2])
        
        main(invader_data, defender_data)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
        