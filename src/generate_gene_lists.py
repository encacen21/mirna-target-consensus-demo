from pathlib import Path
import pandas as pd


def main():
    consensus_path = Path("results/expected/consensus/mirna_target_consensus.tsv")
    output_dir = Path("results/expected/gene_lists")
    output_dir.mkdir(parents=True, exist_ok=True)

    if not consensus_path.exists():
        raise FileNotFoundError(
            f"Missing consensus file: {consensus_path}. "
            "Run src/build_consensus.py first."
        )

    consensus = pd.read_csv(consensus_path, sep="\t")

    required_columns = {"mirna_id", "gene_symbol"}
    missing = required_columns - set(consensus.columns)
    if missing:
        raise ValueError(f"Consensus table is missing required columns: {missing}")

    written = 0

    for mirna_id, subset in consensus.groupby("mirna_id"):
        genes = (
            subset["gene_symbol"]
            .dropna()
            .drop_duplicates()
            .sort_values()
        )

        safe_mirna_id = mirna_id.replace("/", "_").replace(" ", "_")
        output_path = output_dir / f"{safe_mirna_id}_targets.txt"

        genes.to_csv(output_path, index=False, header=False)
        written += 1

    print(f"Wrote gene lists for {written} mock miRNAs to {output_dir}")


if __name__ == "__main__":
    main()
