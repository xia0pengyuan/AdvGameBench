# src/advgamebench/cli.py

import argparse
from advgamebench.core.runner import run_all  

def main() -> int:
    parser = argparse.ArgumentParser(prog="advgamebench")
    parser.add_argument("--games", nargs="+", default=["Tower_Defense"])
    parser.add_argument("--models", nargs="+", required=True)
    
    args = parser.parse_args()

    run_all(args)    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
