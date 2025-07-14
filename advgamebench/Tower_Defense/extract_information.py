import prompt as p
import re

KEY_STATS = ("hp", "cost", "dmg", "shot", "speed", "range")
_unit_pattern = re.compile(r"^(?P<name>\w+)\s*:\s*(?P<body>.+)$", re.I)

def _build_desc_map(raw_text: str):
    desc_map = {}
    for line in raw_text.strip().splitlines():
        m = _unit_pattern.match(line.strip())
        if not m:
            continue
        name = m["name"]
        tokens = [t.strip() for t in re.split(r",\s*", m["body"])]
        stat_tok, desc_tok = [], []
        for t in tokens:
            if t and t.split()[0].lower().rstrip("s") in KEY_STATS:
                stat_tok.append(t.replace("shot every ", "shot "))
            else:
                desc_tok.append(t)
        desc_map[name] = {
            "stats": ", ".join(stat_tok),
            "desc": "; ".join(desc_tok)
        }
    return desc_map

def _describe_units(data, raw_prompt, extra_note=""):
    desc_map = _build_desc_map(raw_prompt)
    names = {u["name"] for u in data}
    parts = [extra_note] if extra_note else []
    for name in sorted(names):
        info = desc_map.get(name)
        if not info:
            continue
        line = f"{name}: {info['stats']}"
        if info["desc"]:
            line += f"; {info['desc']}"
        parts.append(line)
    return "; ".join(parts)

def describe_humans(data):
    return _describe_units(data.get("humans", []), p.human)

def describe_demons(data):
    return _describe_units(
        data.get("demons", []),
        p.demon,
        extra_note="Default speed 2 (14 s grid‑to‑grid)"
    )