import subprocess
import sys
from pathlib import Path


STEPS = [
    "src/normalize_predictions.py",
    "src/build_consensus.py",
    "src/generate_gene_lists.py",
    "src/summarize_support.py",
]


def main():
    repo_root = Path(__file__).resolve().parents[1]

    for step in STEPS:
        step_path = repo_root / step
        print(f"\nRunning {step}")
        subprocess.run([sys.executable, str(step_path)], check=True, cwd=repo_root)

    print("\nDemo completed successfully.")


if __name__ == "__main__":
    main()
