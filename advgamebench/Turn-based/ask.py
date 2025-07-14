import json
import re
import os
import pandas as pd
import src.advgamebench.core.LLMs as llms
import prompt as p

BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(BASE_DIR, 'eval_results')
os.makedirs(RESULTS_DIR, exist_ok=True)

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


def call_model(model_name: str, prompt: str) -> float:
    """
    调用指定 LLM API 并解析返回结果，确保输出为浮点数。
    """
    try:
        caller = MODEL_CALLERS[model_name]
    except KeyError:
        raise ValueError(f"Unknown model: {model_name}")
    raw = caller(prompt)
    match = re.search(r"\d*\.?\d+", raw)
    if not match:
        raise ValueError(f"{model_name} 返回无法解析的结果: {raw}")
    return float(match.group())


def load_cost_from_csv(test_role: str,
                       test_model: str,
                       tag: str,
                       rnd: int) -> int:
    """
    返回 test_model 在第 rnd 轮的 cost。
    如果 test_role == 'defender' 取 defender_cost，否则取 invader_cost。
    """
    root = "defender_results" if test_role.lower() == "defender" else "invader_results"
    csv_path = os.path.join(BASE_DIR, root, tag,
                            f"{test_model.replace('/', '-')}_results.csv")
    df = pd.read_csv(csv_path)
    row = df.loc[df['round'] == rnd]
    if row.empty:
        raise ValueError(f"找不到第 {rnd} 轮的成本: {csv_path}")
    row = row.iloc[0]
    return int(row['defender_cost'] if test_role.lower() == 'defender' else row['invader_cost'])


def load_round_json(test_role: str,
                    defender_model: str,
                    invader_model: str,
                    tag: str,
                    rnd: int) -> tuple[dict, dict]:
    """
    返回 (defender_json, invader_json)。若找不到指定轮次文件，则降级到初始阵容。
    """
    def build_path(root: str, model: str) -> str:
        filename = f"{model}-round_{rnd}.json"
        return os.path.join(BASE_DIR, root, model.replace('/', '-'), tag, filename)

    try:
        if test_role.lower() == 'defender':
            d_path = build_path('defender_results', invader_model)
            i_path = build_path('invader_results', defender_model)
        else:
            d_path = build_path('defender_results', defender_model)
            i_path = build_path('invader_results', invader_model)
        with open(d_path, 'r', encoding='utf-8') as f:
            defender_json = json.load(f)
        with open(i_path, 'r', encoding='utf-8') as f:
            invader_json = json.load(f)
    except FileNotFoundError:
        init_dir = os.path.join(BASE_DIR, 'initial_placements')
        with open(os.path.join(init_dir, f"{defender_model.replace('/', '-')}_defender.json"), 'r', encoding='utf-8') as f:
            defender_json = json.load(f)
        with open(os.path.join(init_dir, f"{invader_model.replace('/', '-')}_invader.json"), 'r', encoding='utf-8') as f:
            invader_json = json.load(f)
    return defender_json, invader_json


def make_eval_prompt(own_json: dict,
                     opp_json: dict,
                     side: str,
                     cost: int,
                     budget: int,
                     scenario: str) -> str:
    scenario = scenario.upper()
    if scenario == 'SELF':
        modifier_text = 'Note: You just modified the lineup above yourself.'
    elif scenario == 'OTHER':
        modifier_text = 'Note: The above lineup was modified by another model, not by you.'
    else:
        modifier_text = ''

    own_str = json.dumps(own_json, ensure_ascii=False, separators=(',', ':'))
    opp_str = json.dumps(opp_json, ensure_ascii=False, separators=(',', ':'))

    return f"""
You are playing as the {side} in this game.
Your cost was {cost}, budget is {budget}.
If you exceed your budget, you will lose the match.
{modifier_text}

Game Rules:
{p.rule}

Your unit catalogue:
{p.defender if side=='Defender' else p.invader}

Opponent unit catalogue:
{p.invader if side=='Invader' else p.defender}

Opponent JSON:
{opp_str}

Your {side.lower()} JSON:
{own_str}

Goal:
Please do NOT modify any lineup and do NOT output JSON.
Please output ONLY the estimated win probability as a decimal between 0 and 1.
"""


def evaluate_one_round(model_name: str,
                       test_role: str,
                       defender_model: str,
                       invader_model: str,
                       tag: str,
                       rnd: int,
                       defender_budget: int = 20,
                       invader_budget: int = 20,
                       scenario: str = 'NONE') -> float:
    defender_json, invader_json = load_round_json(
        test_role, defender_model, invader_model, tag, rnd)
    test_model = defender_model if test_role.lower() == 'defender' else invader_model
    cost = load_cost_from_csv(test_role, test_model, tag, rnd)
    side, budget = ('Defender', defender_budget) if test_role.lower() == 'defender' else ('Invader', invader_budget)
    own_json, opp_json = (defender_json, invader_json) if side == 'Defender' else (invader_json, defender_json)
    prompt = make_eval_prompt(own_json, opp_json, side, cost, budget, scenario)
    return call_model(model_name, prompt)


def main():
    # 批量评估示例，并存储结果
    defender_model = 'chatgpt-4o'
    invader_model  = 'chatgpt-o3-mini'
    tag, rnd = 'first', 1

    records = []
    for model_name in ['chatgpt-4o', 'chatgpt-o3-mini']:
        for scenario in ['SELF', 'OTHER', 'NONE']:
            prob = evaluate_one_round(
                model_name=model_name,
                test_role='defender',
                defender_model=defender_model,
                invader_model=invader_model,
                tag=tag,
                rnd=rnd,
                scenario=scenario
            )
            print(f"Model={model_name} Scenario={scenario} Round={rnd} -> WinProb={prob}")
            records.append({
                'model': model_name,
                'scenario': scenario,
                'round': rnd,
                'win_prob': prob
            })
    # 存储所有评估结果
    df = pd.DataFrame(records)
    outfile = os.path.join(RESULTS_DIR, f'eval_{tag}_round{rnd}.csv')
    df.to_csv(outfile, index=False)
    print(f"Saved evaluation results to {outfile}")

if __name__ == '__main__':
    main()
