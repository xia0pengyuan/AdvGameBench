import re
import prompt as p

import re

def extract_costs(info_text):
    """
    从 info_text 中提取 cost 映射，key 全部小写
    """
    costs = {}
    for line in info_text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # 名称：行首连续字母/数字/下划线
        m = re.match(r"^(\w+)", line)
        if not m:
            continue
        name = m.group(1).lower()
        # cost 后跟数字
        cm = re.search(r"cost\s*(\d+)", line)
        if cm:
            costs[name] = int(cm.group(1))
    return costs

def budget_calculator(map_data):
    """
    统一处理 defenders 和 invaders
    """
    total = 0

    # 先检查 defenders
    if "defenders" in map_data:
        cost_map = extract_costs(p.defender)
        units = map_data["defenders"]
    # 再检查 invaders
    elif "invaders" in map_data:
        cost_map = extract_costs(p.invader)
        units = map_data["invaders"]
    else:
        return 0

    for u in units:
        name = u.get("name", "").lower()       # 小写匹配
        base = cost_map.get(name, 0)
        # 如果是金色，乘3
        if u.get("tier", "").lower() == "gold":
            base *= 3
        total += base

    return total
