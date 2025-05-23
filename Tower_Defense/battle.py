import subprocess
import os
import prompt as p
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import LLMs as llms
import json
from calculator import budget_calculator
from extract_information import describe_humans, describe_demons
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
    match = re.search(pattern, rsp, re.DOTALL)
    code_text = match.group(1) if match else rsp
    code_text = code_text.strip()
    if (code_text.startswith('"') and code_text.endswith('"')) or (code_text.startswith("'") and code_text.endswith("'")):
        code_text = code_text[1:-1].strip()
    code_text = code_text.replace('\\n', '\n')
    if "'" in code_text and '"' not in code_text:
        code_text = code_text.replace("'", '"')
    parsed = json.loads(code_text)
    data = json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
    return json.loads(data)

def run_game_script(human_data, demon_data):

    if not os.path.exists(os.path.join(BASE_DIR, "game_scripts", "run.py")):
        print("Game script run.py does not exist.")
        sys.exit(1)
    try:
        result = subprocess.run(["python", os.path.join(BASE_DIR, "game_scripts", "run.py"),json.dumps(human_data),json.dumps(demon_data)], check=True, capture_output=True, text=True)
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

    opp_human_catalogue = describe_humans(opp_json)
    opp_demon_catalogue = describe_demons(opp_json)

    return f"""
    You are playing as the {side} in this game.
    Last round result: {result} won the game.
    Your previous json cost was {cost}, budget is {budget}.
    if you exceed your budget, you will lose the match

    Game Rules:
    {p.rule}

    Your unit catalogue:
    {p.human if side=='Human' else p.demon}

    Opponent unit catalogue:
    {opp_human_catalogue if side=='Demon' else opp_demon_catalogue}

    Your previous {side.lower()} JSON:
    {json.dumps(last_json, ensure_ascii=False)}

    Opponent JSON:
    {json.dumps(opp_json, ensure_ascii=False)}

    Goal:
    Regenerate and return a single JSON object with the key "{side.lower()}s"
    so that you maximize the chance of winning. Do not include any other text.
    """

def decide_winner(human_cost, demon_cost,
                  human_budget, demon_budget,
                  winner):

    over_human = max(human_cost - human_budget, 0)
    over_demon = max(demon_cost - demon_budget, 0)

    if over_human == 0 and over_demon > 0:
        return "Human"
    if over_demon == 0 and over_human > 0:
        return "Demon"


    if over_human == 0 and over_demon == 0:
        return winner  

    pct_human = over_human / human_budget
    pct_demon = over_demon / demon_budget
    if pct_human < pct_demon:
        return "Human"
    if pct_demon < pct_human:
        return "Demon"

def main_loop(
    human_LLM: str,
    demon_LLM: str,
    human_budget: int,
    demon_budget: int,
    tag: str,
    rounds: int = 10,
    human_first: bool = True,
    test_role: str = "human",   
) -> pd.DataFrame:
    """
    Run multiple rounds of Human vs. Demon match-ups.
    Records cost, winner, lost grid row, and remaining stats each round.

    Args:
        human_LLM: Model name controlling Human side.
        demon_LLM: Model name controlling Demon side.
        human_budget: Budget cap for Human units.
        demon_budget: Budget cap for Demon units.
        tag:       'first' or 'second' mover tag for filtering.
        rounds:    Number of update rounds to execute.
        human_first: If True, Human acts first each round.
        test_role: Which side to evaluate ("human" or "demon").

    Returns:
        DataFrame of per-round records.
    """
    path_model = human_LLM if test_role.lower() == "human" else demon_LLM
    test_model = demon_LLM if test_role.lower() == "human" else human_LLM
    # Helper to load JSON placement for given role and model
    def _load_json(role: str, model: str):
        fname = f"{model.replace('/', '-')}_{role}.json"
        path = os.path.join(os.path.dirname(__file__),
                            'initial_placements', fname)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    human_json = _load_json("human", human_LLM)
    demon_json = _load_json("demon", demon_LLM)

    records = []

    update_order = ["Human", "Demon"] if human_first else ["Demon", "Human"]

    for i in range(1, rounds):
        out = run_game_script(human_json, demon_json)
        lost_row = remain_chars = remain_cost = None
        m = re.search(
            r"Lost grid row:\s*(\d+)\s*\|\s*remain characters:\s*(\d+),\s*cost:\s*(\d+)",
            out,
        )
        if m:
            lost_row     = int(m.group(1))
            remain_chars = int(m.group(2))
            remain_cost  = int(m.group(3))

        human_cost = budget_calculator(human_json)
        demon_cost = budget_calculator(demon_json)
        raw_winner = out.split()[0] if out.split() else None
        winner = decide_winner(
            human_cost, demon_cost,
            human_budget, demon_budget,
            raw_winner
        )

        records.append({
            "round":               i,
            "side":                None,     
            "human_cost":          human_cost,
            "demon_cost":          demon_cost,
            "winner":              winner,
            "lost_row":            lost_row,
            "winner_remain_chars": remain_chars,
            "winner_remain_cost":  remain_cost,
            "human_LLM":           human_LLM,
            "demon_LLM":           demon_LLM,
        })
        # Determine which side updates placement this turn
        side = update_order[(i - 1) % 2]
        if side == "Human":
            model       = human_LLM
            last_json   = human_json
            opp_json    = demon_json
            budget      = human_budget
            cost        = human_cost
        else:  # "Demon"
            model       = demon_LLM
            last_json   = demon_json
            opp_json    = human_json
            budget      = demon_budget
            cost        = demon_cost

        # Build prompt, call model, and update JSON state
        prompt  = make_prompt(side, last_json, opp_json, winner, budget, cost)
        updated = call_model(model, prompt)

        if side == "Human":
            human_json = updated
        else:
            demon_json = updated

        save_root = "human_results" if test_role.lower() == "human" else "demon_results"
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

    final_out = run_game_script(human_json, demon_json)

    lost_row = final_remain_chars = final_remain_cost = None
    m = re.search(
        r"Lost grid row:\s*(\d+)\s*\|\s*remain characters:\s*(\d+),\s*cost:\s*(\d+)",
        final_out,
    )
    if m:
        lost_row           = int(m.group(1))
        final_remain_chars = int(m.group(2))
        final_remain_cost  = int(m.group(3))

    final_human_cost = budget_calculator(human_json)
    final_demon_cost = budget_calculator(demon_json)
    raw_winner = final_out.split()[0] if final_out.split() else None
    winner = decide_winner(
        final_human_cost, final_demon_cost,
        human_budget, demon_budget,
        raw_winner
    )

    records.append({
        "round":               rounds,
        "side":                None,
        "human_cost":          final_human_cost,
        "demon_cost":          final_demon_cost,
        "winner":              winner,
        "lost_row":            lost_row,
        "winner_remain_chars": final_remain_chars,
        "winner_remain_cost":  final_remain_cost,
        "human_LLM":           human_LLM,
        "demon_LLM":           demon_LLM,
    })

    return pd.DataFrame(records)
    
if __name__ == "__main__":

    HUMAN_BUDGET = 2000
    DEMON_BUDGET = 1500

# Configuration: test both roles acting first or second
    settings = [
        ("human",  True, "first"),
        ("human",  False, "second"),
        ("demon",  False, "first"),
        ("demon",  True, "second")
    ]

    for root in ("human_results", "demon_results"):
        for tag in ("first", "second"):
            path = os.path.join(BASE_DIR, root, tag)
            os.makedirs(path, exist_ok=True)

    for role, human_first, tag in settings:
        for test_model in models:
            for fixed_model in fix_models:
                if role == "human":
                    human_model, demon_model = test_model, fixed_model
                    result_root = "human_results"
                else:
                    human_model, demon_model = fixed_model, test_model
                    result_root = "demon_results"

                csv_dir = os.path.join(BASE_DIR, result_root, tag)
                os.makedirs(csv_dir, exist_ok=True)
                csv_path = os.path.join(
                    csv_dir,
                    f"{test_model.replace('/', '-')}_results.csv"
                )


                df = main_loop(
                    human_LLM   = human_model,
                    demon_LLM   = demon_model,
                    human_budget= HUMAN_BUDGET,
                    demon_budget=  DEMON_BUDGET,
                    tag=tag,
                    rounds = rounds,
                    human_first = human_first,
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
