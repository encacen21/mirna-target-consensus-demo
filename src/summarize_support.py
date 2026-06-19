from pathlib import Path
import pandas as pd


def main():
    normalized_path = Path("results/expected/normalized/all_predictions_long.tsv")
    consensus_path = Path("results/expected/consensus/mirna_target_consensus.tsv")
    output_dir = Path("results/expected/summary")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not normalized_path.exists():
        raise FileNotFoundError(
            f"Missing normalized predictions file: {normalized_path}. "
            "Run src/normalize_predictions.py first."
        )

    if not consensus_path.exists():
        raise FileNotFoundError(
            f"Missing consensus file: {consensus_path}. "
            "Run src/build_consensus.py first."
        )

    normalized = pd.read_csv(normalized_path, sep="\t")
    consensus = pd.read_csv(consensus_path, sep="\t")

    required_normalized = {"mirna_id", "target_id", "tool"}
    missing_normalized = required_normalized - set(normalized.columns)
    if missing_normalized:
        raise ValueError(f"Normalized table is missing required columns: {missing_normalized}")

    required_consensus = {"mirna_id", "target_id", "consensus_level", "tool_support_n"}
    missing_consensus = required_consensus - set(consensus.columns)
    if missing_consensus:
        raise ValueError(f"Consensus table is missing required columns: {missing_consensus}")

    tool_summary = (
        normalized
        .groupby("tool", as_index=False)
        .agg(
            prediction_count=("target_id", "count"),
            unique_targets=("target_id", "nunique"),
            unique_mirnas=("mirna_id", "nunique"),
        )
        .sort_values(by=["prediction_count", "tool"], ascending=[False, True])
    )

    consensus_level_summary = (
        consensus
        .groupby("consensus_level", as_index=False)
        .agg(
            interaction_count=("target_id", "count"),
            mean_tool_support=("tool_support_n", "mean"),
        )
    )

    consensus_order = {
        "high": 0,
        "medium": 1,
        "single_tool": 2,
    }

    consensus_level_summary["rank"] = consensus_level_summary["consensus_level"].map(consensus_order)

    consensus_level_summary = (
        consensus_level_summary
        .sort_values(by="rank")
        .drop(columns="rank")
        .reset_index(drop=True)
    )

    tool_summary_path = output_dir / "tool_support_summary.tsv"
    consensus_summary_path = output_dir / "consensus_level_summary.tsv"

    tool_summary.to_csv(tool_summary_path, sep="\t", index=False)
    consensus_level_summary.to_csv(consensus_summary_path, sep="\t", index=False)

    print(f"Wrote tool summary to {tool_summary_path}")
    print(f"Wrote consensus-level summary to {consensus_summary_path}")


if __name__ == "__main__":
    main()
