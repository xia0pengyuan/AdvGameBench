import prompt as p
import re

def describe_defenders(data):

    pattern = re.compile(r'^(\w+)\s*\(\s*atk(\d+)\s+hp(\d+)\s+cost(\d+)\s*\)\s*(.+)$')
    desc_map = {}
    for line in p.defender.strip().splitlines():
        m = pattern.match(line.strip())
        if m:
            name, atk, hp, cost, desc = m.groups()
            desc_map[name] = {
                'stats': f"atk{atk}, hp{hp}, cost{cost}",
                'description': desc
            }

    lines = []
    for d in data.get('defenders', []):
        name = d.get('name')
        info = desc_map.get(name)
        if info:
            lines.append(
                f"{name}s: {info['stats']}. Description: {info['description']}."
            )

    return "\n".join(lines)

def describe_invaders(data):

    pattern = re.compile(r'^(\w+)\s*\(\s*atk(\d+)\s+hp(\d+)\s+cost(\d+)\s*\)\s*(.+)$')
    desc_map = {}
    for line in p.invader.strip().splitlines():
        m = pattern.match(line.strip())
        if m:
            name, atk, hp, cost, desc = m.groups()
            desc_map[name] = {
                'stats': f"atk{atk}, hp{hp}, cost{cost}",
                'description': desc
            }

    lines = []
    for d in data.get('invaders', []):
        name = d.get('name')
        info = desc_map.get(name)
        if info:
            lines.append(
                f"{name}s: {info['stats']}. Description: {info['description']}."
            )

    return "\n".join(lines)