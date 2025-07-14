import re
import prompt as p

_HUMAN_COST_MAP = {}
_DEMON_COST_MAP = {}

def extract_costs(text):
    cost_dict = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or ':' not in line:
            continue
        unit_name, rest = line.split(":", 1)
        unit_name = unit_name.strip()
        m = re.search(r"cost[:\s]+(\d+)", rest)
        if m:
            cost_dict[unit_name] = int(m.group(1))
    return cost_dict

_HUMAN_COST_MAP = extract_costs(p.human)
_DEMON_COST_MAP = extract_costs(p.demon)


def budget_calculator(map_data):

    total_cost = 0

    if "humans" in map_data:
        for unit in map_data["humans"]:
            name = unit.get("name", "")
            total_cost += _HUMAN_COST_MAP.get(name, 0)

    elif "demons" in map_data:
        for unit in map_data["demons"]:
            name = unit.get("name", "")
            total_cost += _DEMON_COST_MAP.get(name, 0)

    return total_cost
