import re
import prompt as p

def extract_costs(info_text):
    costs = {}
    for line in info_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\w+)", line)
        if not m:
            continue
        name = m.group(1).lower()
        cm = re.search(r"cost\s*(\d+)", line)
        if cm:
            costs[name] = int(cm.group(1))
    return costs

def budget_calculator(map_data):
    total = 0

    if "defenders" in map_data:
        cost_map = extract_costs(p.defender)
        units = map_data["defenders"]
    elif "invaders" in map_data:
        cost_map = extract_costs(p.invader)
        units = map_data["invaders"]
    else:
        return 0

    for u in units:
        name = u.get("name", "").lower()      
        base = cost_map.get(name, 0)
        if u.get("tier", "").lower() == "gold":
            base *= 3
        total += base

    return total
