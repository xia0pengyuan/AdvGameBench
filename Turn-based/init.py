import os
import sys
import json
import re
# Ensure project root is on PYTHONPATH for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import prompt as p
from calculator import budget_calculator
import LLMs as llms

# Load model lists from environment
primary_models = json.loads(os.getenv('MODELS', '[]'))
fixed_models = json.loads(os.getenv('FIX_MODELS', '[]'))
if not primary_models:
    raise RuntimeError('No MODELS provided in environment')

# Combine and dedupe models for init stage
models = list(dict.fromkeys(primary_models + fixed_models))

# Budget constants
DEFENDER_BUDGET = 20
INVADER_BUDGET = 20

# Paths
BASE_DIR = os.path.dirname(__file__)
EXAMPLE_DIR = os.path.join(BASE_DIR, 'example_placement')
OUTPUT_DIR = os.path.join(BASE_DIR, 'initial_placements')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping model names to caller functions
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
    'llama-3-70B':       llms.call_meta_llama_70B_api,
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

def call_model(model_name, prompt_text):
    if model_name not in MODEL_CALLERS:
        raise ValueError(f"Unknown model: {model_name}")
    return parse_code(MODEL_CALLERS[model_name](prompt_text))


def generate_initial_placement(model: str, side: str, example: dict, budget: int, retries: int = 3) -> dict:
    """
    Generate a placement JSON for given side, retrying if cost > budget.
    """
    prompt_template = f"""
You are the {side} side.
Your task is to purchase characters/units and arrange them to maximize your chances of winning.
Your total budget for {side.lower()} is {budget}.

Game Rules:
{p.rule}

{side} Unit Information:
{getattr(p, side.lower())}

Example {side} JSON:
{json.dumps(example, ensure_ascii=False)}

Important: your output must be a single JSON object with the key "{side.lower()}s" and must not include any other text or explanation.
"""
    feedback = ''
    for attempt in range(1, retries + 1):
        full_prompt = prompt_template + ('\n' + feedback if feedback else '')
        placement = call_model(model, full_prompt)   
        cost = budget_calculator(placement)
        if cost <= budget:
            return placement
        feedback = (f'[Attempt {attempt}] cost {cost} > budget {budget}. '
                    f'Adjust layout. Previous output:\n{json.dumps(placement, indent=2)}')
    return placement


def load_example(side: str) -> dict:
    """
    Load example JSON for 'defender' or 'invader'.
    """
    path = os.path.join(EXAMPLE_DIR, f'{side.lower()}_example.json')
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    defender_example = load_example('defender')
    invader_example  = load_example('invader')

    for model in models:
        def_pl = generate_initial_placement(model, 'Defender', defender_example, DEFENDER_BUDGET)
        inv_pl = generate_initial_placement(model, 'Invader', invader_example, INVADER_BUDGET)

        def_file = os.path.join(OUTPUT_DIR, f'{model.replace("/", "-")}_defender.json')
        inv_file = os.path.join(OUTPUT_DIR, f'{model.replace("/", "-")}_invader.json')

        with open(def_file, 'w', encoding='utf-8') as f:
            json.dump(def_pl, f, ensure_ascii=False, indent=2)
        with open(inv_file, 'w', encoding='utf-8') as f:
            json.dump(inv_pl, f, ensure_ascii=False, indent=2)



if __name__ == '__main__':
    main()