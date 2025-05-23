import subprocess
import os
import prompt as p
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import LLMs as llms
import json
from calculator import budget_calculator
from extract_information import describe_defenders, describe_invaders
import re

models  = json.loads(os.getenv('MODELS', '[]'))
fix_models = json.loads(os.getenv('FIX_MODELS', '[]'))
rounds = int(os.getenv('ROUNDS', '10'))
if not models:
    raise RuntimeError("No MODELS provided in environment")

BASE_DIR = os.path.dirname(__file__) 
INIT_DIR = os.path.join(BASE_DIR, 'initial_placements')

MODEL_CALLERS = {
    'chatgpt-o3':        llms.call_chatgpt_o3_api,
    'chatgpt-4o':        llms.call_chatgpt_4o_api,
    'deepSeek-V3':       llms.call_deepseek_V3_api,
    'deepSeek-R1':       llms.call_deepseek_R1_api,
    'qwen-max':          llms.call_qwen_max_api,
    'qwen-plus':         llms.call_qwen_plus_api,
    'claude-3-5-sonnet': llms.call_claude_35_sonnet_api,
    'chatgpt-o3-mini':   llms.call_chatgpt_o3_mini_api,
    'chatgpt-4.1':       llms.call_chatgpt_41_api,
    'gemini-2-flash':    llms.call_gemini_2_flash_api,
    'gemini-2.5-flash':  llms.call_gemini_2_5_flash_api,
    'llama-3-70B':       llms.call_meta_llama_70B_api
}

def parse_code(rsp):
    pattern = r'```json(.*)```'
    match   = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp

    code_text = code_text.strip()

    if ((code_text.startswith('"') and code_text.endswith('"')) or
        (code_text.startswith("'") and code_text.endswith("'"))):
        code_text = code_text[1:-1].strip()

    code_text = code_text.replace('\\n', '\n')

    if "'" in code_text and '"' not in code_text:
        code_text = code_text.replace("'", '"')

    if code_text.rstrip().endswith('}}'):
        code_text = code_text.rstrip()[:-1]
    code_text = re.sub(r'["\']\s*}$', '}', code_text)


    parsed = json.loads(code_text)

    data = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
    return json.loads(data)

def run_game_script(human_data, demon_data):

    if not os.path.exists(os.path.join(BASE_DIR, "game_scripts", "main.py")):
        print("Game script main.py does not exist.")
        sys.exit(1)
    try:
        result = subprocess.run(["python", os.path.join(BASE_DIR, "game_scripts", "main.py"),json.dumps(human_data),json.dumps(demon_data)], check=True, capture_output=True, text=True)
        output = result.stdout.strip()
        lines = output.splitlines()  
        result = lines[-1]  

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the game script: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    
    return result

def call_model(model_name, prompt):
    try:
        caller = MODEL_CALLERS[model_name]
    except KeyError:
        raise ValueError(f"Unknown model: {model_name}")
    #print(f"[Calling] {model_name}")
    
    return parse_code(caller(prompt))

def make_prompt(side, last_json, opp_json, result, budget, cost):
    defender_catalogue = p.defender
    invader_catalogue = p.invader

    opp_defender_catalogue = describe_defenders(opp_json)
    opp_invader_catalogue = describe_invaders(opp_json)

    return f"""
    You are playing as the {side} in this game.
    Last round result: {result}
    Your cost was {cost}, budget is {budget}.
    if you exceed your budget, you will lose the match

    Game Rules:
    {p.rule}

    Your unit catalogue:
    {defender_catalogue if side=='Defender' else invader_catalogue}

    Opponent unit catalogue:
    {opp_defender_catalogue if side=='Invader' else opp_invader_catalogue}

    Opponent JSON:
    {json.dumps(opp_json, ensure_ascii=False)}

    Your previous {side.lower()} JSON:
    {json.dumps(last_json, ensure_ascii=False)}

    Goal:
    Regenerate and return a single JSON object with the key **{side.lower()}s**
    so that you maximize the chance of winning. Do not include any other text.
    """

def decide_winner(defender_cost, invader_cost,
                  defender_budget, invader_budget,
                  winner):
    over_defender = max(defender_cost - defender_budget, 0)
    over_invader  = max(invader_cost  - invader_budget, 0)

    if over_defender == 0 and over_invader > 0:
        return "Defenders"
    if over_invader  == 0 and over_defender > 0:
        return "Invaders"


    if over_defender == 0 and over_invader == 0:
        return winner   

    pct_defender = over_defender / defender_budget
    pct_invader  = over_invader  / invader_budget
    if pct_defender < pct_invader:
        return "Defenders"
    if pct_invader  < pct_defender:
        return "Invaders"

def main_loop(
    defender_LLM: str,
    invader_LLM: str,
    defender_budget: int,
    invader_budget: int,
    tag:str,
    rounds: int = 10,
    defender_first: bool = True,
    test_role: str = "defender",
) -> pd.DataFrame:
    
    path_model = defender_LLM if test_role.lower() == "defender" else invader_LLM
    test_model = invader_LLM if test_role.lower() == "defender" else defender_LLM

    def _load_json(role: str, model: str):
        fname = f"{model.replace('/', '-')}_{role}.json"
        # 之前： path = os.path.join("./initial_placements", fname)
        path = os.path.join(os.path.dirname(__file__),
                            'initial_placements', fname)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing init file: {path}")
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    defender_json = _load_json("defender", defender_LLM)
    invader_json = _load_json("invader", invader_LLM)

    records = []

    update_order = ["Defender", "Invader"] if defender_first else ["Invader", "Defender"]

    for i in range(1, rounds + 1):
        out = run_game_script(defender_json, invader_json)
        winner = out.split()[0] if out.split() else None

        defender_cost = budget_calculator(defender_json)
        invader_cost = budget_calculator(invader_json)
        raw_winner = out.split()[0] if out.split() else None
        winner = decide_winner(
            defender_cost, invader_cost,
            defender_budget, invader_budget,
            raw_winner
        )

        records.append({
            "round":         i,
            "defender_cost": defender_cost,
            "invader_cost":  invader_cost,
            "winner":        winner,
            "invader_LLM":   invader_LLM,
            "defender_LLM":  defender_LLM
        })

        side = update_order[(i - 1) % 2]
        if side == "Defender":
            model       = defender_LLM
            last_json   = defender_json
            opp_json    = invader_json
            budget      = defender_budget
            cost        = defender_cost
        else:  # "Demon"
            model       = invader_LLM
            last_json   = invader_json
            opp_json    = defender_json
            budget      = invader_budget
            cost        = invader_cost

        prompt  = make_prompt(side, last_json, opp_json, winner, budget, cost)
        updated = call_model(model, prompt)

        if side == "Defender":
            defender_json = updated
        else:
            invader_json = updated


        save_root = "defender_results" if test_role.lower() == "defender" else "invader_results"
        save_dir = os.path.join(
            BASE_DIR,
            save_root,
            path_model.replace("/", "-"),
            tag
        )
        os.makedirs(save_dir, exist_ok=True)

        with open(os.path.join(save_dir, f"{test_model}-round_{i}.json"),
                    "w", encoding="utf-8") as f:
            json.dump(updated, f, ensure_ascii=False, indent=2)

    final_out = run_game_script(defender_json, invader_json)

    final_defender_cost = budget_calculator(defender_json)
    final_invader_cost = budget_calculator(invader_json)
    raw_winner = final_out.split()[0] if final_out.split() else None
    winner = decide_winner(
        final_defender_cost, final_invader_cost,
        defender_budget, invader_budget,
        raw_winner
    )

    records.append({
        "round":         rounds,
        "defender_cost": final_defender_cost,
        "invader_cost":  final_invader_cost,
        "winner":        winner,
        "invader_LLM":   invader_LLM,
        "defender_LLM":  defender_LLM
        })

    return pd.DataFrame(records)
    
    
if __name__ == "__main__":

    defender_budget = 20
    invader_budget = 20


settings = [
    ("defender",  True, "first"),
    ("defender",  False, "second"),
    ("invader",  False, "first"),
    ("invader",  True, "second")  
]

for root in ("defender_results", "invader_results"):
    for tag in ("first", "second"):
        path = os.path.join(BASE_DIR, root, tag)
        os.makedirs(path, exist_ok=True)

for role, defender_first, tag in settings:
    for test_model in models:
        for fixed_model in fix_models:
            if role == "defender":
                defender_model, invader_model = test_model, fixed_model
                result_root = "defender_results"
            else:
                defender_model, invader_model = fixed_model, test_model
                result_root = "invader_results"

            csv_dir = os.path.join(BASE_DIR, result_root, tag)
            os.makedirs(csv_dir, exist_ok=True)
            csv_path = os.path.join(
                csv_dir,
                f"{test_model.replace('/', '-')}_results.csv"
            )

            df = main_loop(
                defender_LLM   = defender_model,
                invader_LLM   = invader_model,
                defender_budget= defender_budget,
                invader_budget= invader_budget,
                tag = tag,
                rounds = rounds,
                defender_first = defender_first,
                test_role= role
            )

            first_write = not os.path.exists(csv_path)
            df.to_csv(
                csv_path,
                mode='w' if first_write else 'a',
                header=first_write,
                index=False,
                encoding='utf-8'
            )
            #print(f"[{result_root}/{tag}] {test_model} ({role}) vs {fixed_model} → {csv_path}")