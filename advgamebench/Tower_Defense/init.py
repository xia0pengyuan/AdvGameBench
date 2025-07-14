# init.py
# Generates initial unit placements for each LLM model based on provided examples.

import os
import sys
import json
import re
# Add project root to path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import prompt as p
from calculator import budget_calculator
import src.advgamebench.core.LLMs as llms

# Load models from environment variables
primary_models = json.loads(os.getenv('MODELS', '[]'))
fixed_models = json.loads(os.getenv('FIX_MODELS', '[]'))
if not primary_models:
    raise RuntimeError("No MODELS provided in environment")

# For init stage, combine and deduplicate both lists
models = list(dict.fromkeys(primary_models + fixed_models))

# Constants: budgets per side
HUMAN_BUDGET = 2000
DEMON_BUDGET = 1500

# Directories
BASE_DIR = os.path.dirname(__file__)
EXAMPLE_DIR = os.path.join(BASE_DIR, 'example_placement')
OUTPUT_DIR = os.path.join(BASE_DIR, 'initial_placements')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping from model name to caller function
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


def call_model(model_name: str, prompt: str) -> str:
    """
    Send prompt to the specified LLM and return its response.
    """
    if model_name not in MODEL_CALLERS:
        raise ValueError(f"Unknown model: {model_name}")
    output = MODEL_CALLERS[model_name](prompt)
    #print(model_name, output)
    return parse_code(output)


def generate_initial_placement(model: str, side: str, example: dict, budget: int, retries: int = 5) -> dict:
    """
    Generate a unit placement, retrying if cost exceeds budget.
    """
    base_prompt = f"""
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
    feedback = ""

    for i in range(1, retries + 1):
        full_prompt = base_prompt + ("\n" + feedback if feedback else "")
        response = call_model(model, full_prompt)
        cost = budget_calculator(response)

        if cost <= budget:
            return response

        warning = f"[Attempt {i}] cost {cost} exceeds budget {budget}."
        feedback = warning + " Please adjust layout. Previous output: " + json.dumps(response, indent=2)

    return response


with open(os.path.join(EXAMPLE_DIR, 'human_example.json'), encoding='utf-8') as f:
    human_example = json.load(f)
with open(os.path.join(EXAMPLE_DIR, 'demon_example.json'), encoding='utf-8') as f:
    demon_example = json.load(f)

# Generate placements for each model
for m in models:
    human_output = generate_initial_placement(m, 'Human', human_example, HUMAN_BUDGET)
    demon_output = generate_initial_placement(m, 'Demon', demon_example, DEMON_BUDGET)

    human_file = os.path.join(OUTPUT_DIR, f"{m.replace('/', '-')}_human.json")
    demon_file = os.path.join(OUTPUT_DIR, f"{m.replace('/', '-')}_demon.json")

    with open(human_file, 'w', encoding='utf-8') as f:
        json.dump(human_output, f, ensure_ascii=False, indent=2)
    with open(demon_file, 'w', encoding='utf-8') as f:
        json.dump(demon_output, f, ensure_ascii=False, indent=2)

    #print(f"[Saved] {m}: Human -> {human_file}, Demon -> {demon_file}")

#print("[Done] All initial placements generated.")