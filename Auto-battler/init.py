import os
import json
import prompt as p
from calculator import budget_calculator
import LLMs

# Budget constants
DEFENDER_BUDGET = 20
INVADER_BUDGET = 20

OUTPUT_DIR = './initial_placements/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

MODELS = model_names = [
    'llama-3-70B'
]

MODEL_CALLERS = {
    'chatgpt-o3':        LLMs.call_chatgpt_o3_api,
    'chatgpt-4o':        LLMs.call_chatgpt_4o_api,
    'deepSeek-V3':       LLMs.call_deepseek_V3_api,
    'deepSeek-R1':       LLMs.call_deepseek_R1_api,
    'qwen-max':          LLMs.call_qwen_max_api,
    'qwen-plus':         LLMs.call_qwen_plus_api,
    'claude-3-5-sonnet': LLMs.call_claude_35_sonnet_api,
    'chatgpt-o3-mini':   LLMs.call_chatgpt_o3_mini_api,
    'chatgpt-4.1':       LLMs.call_chatgpt_41_api,
    'gemini-2-flash':    LLMs.call_gemini_2_flash_api,
    'gemini-2.5-flash':  LLMs.call_gemini_2_5_flash_api,
    'llama-3-70B':       LLMs.call_meta_llama_70B_api
}

def call_model(model_name, prompt_text):
    if model_name not in MODEL_CALLERS:
        raise ValueError(f"Unknown model: {model_name}")
    return MODEL_CALLERS[model_name](prompt_text)


def generate_initial_placement(model, side, example_json, budget, max_retries=3):

    base_prompt = f"""
You are the {side} side.
Your task is to purchase characters/units and arrange them to maximize your chances of winning.
Your total budget for {side.lower()} is {budget}.

Game Rules:
{p.rule}

{side} Unit Information:
{getattr(p, side.lower())}

Example {side} JSON:
{json.dumps(example_json, ensure_ascii=False)}

Important: your output must be a single JSON object with the key "{side.lower()}s" and must not include any other text or explanation.
"""
    feedback = ""
    for attempt in range(1, max_retries + 1):
        prompt_text = base_prompt + ("\n" + feedback if feedback else "")
        placement = call_model(model, prompt_text)
        cost = budget_calculator(placement)

        if cost <= budget:
            return placement

        warning = (
            f"[Warning] Attempt {attempt}: generated placement cost {cost} which exceeds "
            f"the budget of {budget}.\n"
        )
        feedback = warning + (
            "Please adjust your layout to meet the budget constraints. "
            "Previous placement:\n" + json.dumps(placement, ensure_ascii=False, indent=2)
        )
        print(warning.strip())

    print(f"[Error] {model} {side} placement still exceeds budget after {max_retries} attempts ({cost} > {budget}).")
    return placement


with open('./example_json/defender_example.json', "r", encoding="utf-8") as f:
    defender_example = json.load(f)
with open('./example_json/invader_example.json', "r", encoding="utf-8") as f:
    invader_example = json.load(f)

for model in MODELS:
    defender_pl = generate_initial_placement(model, 'Defender', defender_example, DEFENDER_BUDGET)
    invader_pl  = generate_initial_placement(model, 'Invader',  invader_example,  INVADER_BUDGET)

    defender_fn = f"{model.replace('/', '-')}_defender.json"
    invader_fn  = f"{model.replace('/', '-')}_invader.json"

    with open(os.path.join(OUTPUT_DIR, defender_fn), 'w', encoding='utf-8') as f:
        json.dump(defender_pl, f, ensure_ascii=False, indent=2)
    with open(os.path.join(OUTPUT_DIR, invader_fn), 'w', encoding='utf-8') as f:
        json.dump(invader_pl, f, ensure_ascii=False, indent=2)

    print(f"[Saved] {model}: defender → {defender_fn}, invader → {invader_fn}")

print("[Done] All initial placements generated.")

