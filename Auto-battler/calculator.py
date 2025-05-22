import re
import prompt as p

def normalize_name(name: str) -> str:
    return re.sub(r'[^0-9A-Za-z]+', '_', name).strip('_').lower()

def extract_costs(text: str) -> dict[str, int]:
    cost_dict: dict[str, int] = {}
    pattern = re.compile(
        r'^\s*[-\u2022]?\s*(?P<name>[^:]+?):.*?Cost\s*(?P<cost>\d+)\s*$',
        re.IGNORECASE
    )
    for line in text.splitlines():
        m = pattern.match(line)
        if not m:
            continue
        human_name = m.group('name').strip()
        key = normalize_name(human_name)
        cost = int(m.group('cost'))
        cost_dict[key] = cost
    return cost_dict

def budget_calculator(map_data: dict) -> int:
    total_cost = 0
    invader_cost_map = extract_costs(p.invader)
    defender_cost_map = extract_costs(p.defender)

    if "invaders" in map_data:
        for unit in map_data["invaders"]:
            for skill in unit.get("skills", []):
                total_cost += invader_cost_map.get(skill, 0)
    if "defenders" in map_data:
        for unit in map_data["defenders"]:
            for skill in unit.get("skills", []):
                total_cost += defender_cost_map.get(skill, 0)

    return total_cost

