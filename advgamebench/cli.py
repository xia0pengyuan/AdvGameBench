# src/advgamebench/cli.py

import argparse
from advgamebench.core.runner import run_all   # 你拆出的核心执行逻辑

def main() -> int:
    parser = argparse.ArgumentParser(prog="advgamebench")
    parser.add_argument("--games", nargs="+", default=["Tower_Defense"])
    parser.add_argument("--models", nargs="+", required=True)
    # …根据需要继续添加参数…
    args = parser.parse_args()

    run_all(args)    # 把解析好的 args 传给你的核心函数
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
