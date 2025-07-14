import prompt as p
import re

def _build_skill_map(section_text):
    # Pattern captures skill name and description
    pattern = re.compile(r"-\s*([\w\s']+):\s*(.+?)\.\s*Cost\s*(\d+)")
    skill_map = {}
    for line in section_text.strip().splitlines():
        m = pattern.match(line.strip())
        if m:
            name, desc, cost = m.groups()
            key = name.lower().replace(' ', '_').replace("'", '')
            skill_map[key] = f"{name}: {desc}. Cost {cost}"
    return skill_map

# Prebuild maps for invaders and defenders
_invader_map = {}
for block in p.invader.strip().split('\n\n'):
    # Split header and skills
    header, *skills = block.splitlines()
    element = header.replace(' skills:', '').strip()
    section_text = '\n'.join(skills)
    inv_map = _build_skill_map(section_text)
    _invader_map[element] = inv_map

_defender_map = {}
for block in p.defender.strip().split('\n\n'):
    header, *skills = block.splitlines()
    element = header.replace(' skills:', '').strip()
    section_text = '\n'.join(skills)
    def_map = _build_skill_map(section_text)
    _defender_map[element] = def_map


def describe_defenders(data):
    lines = []
    for d in data.get('defenders', []):
        elem = d.get('element')
        skills = d.get('skills', [])
        mapping = _defender_map.get(elem, {})
        if mapping:
            extracted = [mapping.get(s, f"{s}: <unknown skill>") for s in skills]
            lines.append(f"{elem} skills included:\n  " + '\n  '.join(extracted))
    return "\n\n".join(lines)


def describe_invaders(data):
    lines = []
    for d in data.get('invaders', []):
        elem = d.get('element')
        skills = d.get('skills', [])
        mapping = _invader_map.get(elem, {})
        if mapping:
            extracted = [mapping.get(s, f"{s}: <unknown skill>") for s in skills]
            lines.append(f"{elem} skills included:\n  " + '\n  '.join(extracted))
    return "\n\n".join(lines)
