import argparse
import subprocess
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_stage(game: str, stage: str, env: dict):
    """
    Run a specific stage script for a given game.
    :param game: name of the game folder
    :param stage: one of 'init', 'battle', 'evaluator'
    :param env: environment variables dict
    """
    script = os.path.join(game, f"{stage}.py")
    if not os.path.isfile(script):
        return
    print(f"--> Running {game}/{stage}.py")
    subprocess.run([sys.executable, script], env=env, check=True)


def prepare_env(models, fix_models, rounds) -> dict:
    """
    Prepare environment variables for subprocesses:
      - MODELS: combined primary models and fixed opponents for init
      - FIX_MODELS: fixed opponents for battle/evaluator
      - ROUNDS: number of battle rounds
    """
    env = os.environ.copy()
    env['MODELS'] = json.dumps(models)
    env['FIX_MODELS'] = json.dumps(fix_models)
    env['ROUNDS'] = str(rounds)
    return env


def run_game(game: str, env: dict):
    """
    Execute full pipeline (init, battle, evaluator) for one game.
    """
    print(f"\n=== Starting game: {game} ===")
    run_stage(game, 'init', env)
    run_stage(game, 'battle', env)
    run_stage(game, 'evaluator', env)


def main():
    parser = argparse.ArgumentParser(
        description="Run experiments across specified games, optionally in parallel with custom round count."
    )
    parser.add_argument(
        '--games', nargs='+', required=True,
        help="List of game folders to run (e.g., 'Auto-battler', 'Tower Defense', 'Turn-based')"
    )
    parser.add_argument(
        '--models', nargs='+', required=True,
        help="List of primary LLM model names for this experiment"
    )
    parser.add_argument(
        '--fix-models', nargs='+', default=[],
        help="List of fixed opponent models for battles"
    )
    parser.add_argument(
        '--rounds', type=int, default=10,
        help="Number of rounds to run in the battle stage"
    )
    parser.add_argument(
        '--parallel', action='store_true',
        help="Whether to run each game's pipeline in parallel"
    )
    args = parser.parse_args()

    # prepare base environment with rounds
    base_env = prepare_env(args.models, args.fix_models, args.rounds)

    if args.parallel:
        # run each game's pipeline concurrently
        with ThreadPoolExecutor(max_workers=len(args.games)) as executor:
            futures = {executor.submit(run_game, game, base_env.copy()): game for game in args.games}
            for fut in as_completed(futures):
                fut.result()
    else:
        # run sequentially
        for game in args.games:
            run_game(game, base_env.copy())

if __name__ == "__main__":
    main()