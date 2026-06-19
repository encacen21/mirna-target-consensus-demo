from pathlib import Path
import pandas as pd


CONSENSUS_ORDER = {
    "high": 0,
    "medium": 1,
    "single_tool": 2,
}


def classify_consensus(tool_support_n: int) -> str:
    """
    Assign a simple consensus level based on the number of tools
    supporting a miRNA-target interaction.
    """
    if tool_support_n >= 3:
        return "high"
    if tool_support_n == 2:
        return "medium"
    return "single_tool"


def build_consensus(normalized_predictions: pd.DataFrame, annotation: pd.DataFrame) -> pd.DataFrame:
    """
    Build a consensus table from normalized long-format predictions.

    Each unique mirna_id + target_id pair is summarized by:
    - number of supporting tools
    - list of supporting tools
    - consensus level
    - mock functional annotation
    """
    grouped = (
        normalized_predictions
        .groupby(["mirna_id", "target_id"], as_index=False)
        .agg(
            tool_support_n=("tool", "nunique"),
            tools_supporting=("tool", lambda values: ";".join(sorted(set(values)))),
        )
    )

    grouped["consensus_level"] = grouped["tool_support_n"].apply(classify_consensus)

    merged = grouped.merge(annotation, on="target_id", how="left")

    expected_columns = [
        "mirna_id",
        "target_id",
        "gene_symbol",
        "gene_description",
        "mock_functional_category",
        "tool_support_n",
        "tools_supporting",
        "consensus_level",
    ]

    missing_columns = [col for col in expected_columns if col not in merged.columns]
    if missing_columns:
        raise ValueError(f"Missing expected columns after annotation merge: {missing_columns}")

    merged["consensus_rank"] = merged["consensus_level"].map(CONSENSUS_ORDER)

    final = (
        merged[expected_columns + ["consensus_rank"]]
        .sort_values(
            by=["consensus_rank", "tool_support_n", "mirna_id", "target_id"],
            ascending=[True, False, True, True],
        )
        .drop(columns=["consensus_rank"])
        .reset_index(drop=True)
    )

    return final


def main():
    normalized_path = Path("results/expected/normalized/all_predictions_long.tsv")
    annotation_path = Path("data/mock/mock_gene_annotation.tsv")
    output_dir = Path("results/expected/consensus")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not normalized_path.exists():
        raise FileNotFoundError(
            f"Missing normalized predictions file: {normalized_path}. "
            "Run src/normalize_predictions.py first."
        )

    if not annotation_path.exists():
        raise FileNotFoundError(f"Missing annotation file: {annotation_path}")

    normalized = pd.read_csv(normalized_path, sep="\t")
    annotation = pd.read_csv(annotation_path, sep="\t")

    consensus = build_consensus(normalized, annotation)

    output_path = output_dir / "mirna_target_consensus.tsv"
    consensus.to_csv(output_path, sep="\t", index=False)

    print(f"Wrote {len(consensus)} consensus interactions to {output_path}")


if __name__ == "__main__":
    main()
