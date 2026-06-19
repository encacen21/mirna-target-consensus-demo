from pathlib import Path
import pandas as pd


TOOL_FILES = {
    "miRanda": "mock_miranda_predictions.tsv",
    "RNAhybrid": "mock_rnahybrid_predictions.tsv",
    "psRNATarget": "mock_psrnatarget_predictions.tsv",
    "PTarPmiR": "mock_ptarpmir_predictions.tsv",
}


def normalize_predictions(input_dir: Path) -> pd.DataFrame:
    """
    Read mock prediction files from several tools and convert them into
    one common long-format table.

    Required columns in every input file:
    - mirna_id
    - target_id

    Any additional columns are preserved as a text evidence field.
    """
    records = []

    for tool_name, filename in TOOL_FILES.items():
        path = input_dir / filename

        if not path.exists():
            raise FileNotFoundError(f"Missing input file: {path}")

        df = pd.read_csv(path, sep="\t")

        required = {"mirna_id", "target_id"}
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{filename} is missing required columns: {missing}")

        for _, row in df.iterrows():
            evidence = row.drop(labels=["mirna_id", "target_id"]).to_dict()

            records.append(
                {
                    "mirna_id": row["mirna_id"],
                    "target_id": row["target_id"],
                    "tool": tool_name,
                    "evidence": "; ".join(f"{key}={value}" for key, value in evidence.items()),
                }
            )

    return pd.DataFrame(records)


def main():
    input_dir = Path("data/mock")
    output_dir = Path("results/expected/normalized")
    output_dir.mkdir(parents=True, exist_ok=True)

    normalized = normalize_predictions(input_dir)
    output_path = output_dir / "all_predictions_long.tsv"
    normalized.to_csv(output_path, sep="\t", index=False)

    print(f"Wrote {len(normalized)} normalized prediction records to {output_path}")


if __name__ == "__main__":
    main()
