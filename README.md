# miRNA Target Consensus Demo

This repository is a synthetic portfolio demo showing how predictions from multiple miRNA target-prediction tools can be normalized, integrated, summarized, and converted into consensus-based target tables.

The project uses only mock data. It does not contain unpublished research data, real thesis results, real biological candidates, real sample names, or experimental validation.

## Overview

miRNA target-prediction workflows often produce outputs from multiple tools with different column names, scoring systems, and formats. This demo shows a simple reproducible workflow to:

- read mock prediction outputs from multiple tools;
- normalize predictions into a common long-format table;
- group predictions by `mirna_id` and `target_id`;
- calculate the number of tools supporting each interaction;
- classify interactions into simple consensus levels;
- join mock gene annotations;
- export consensus tables, gene lists, and summary tables.

## Repository Structure

    mirna-target-consensus-demo/
    ├── README.md
    ├── requirements.txt
    ├── LICENSE
    ├── .gitignore
    ├── data/
    │   └── mock/
    │       ├── mock_mirnas.fasta
    │       ├── mock_miranda_predictions.tsv
    │       ├── mock_rnahybrid_predictions.tsv
    │       ├── mock_psrnatarget_predictions.tsv
    │       ├── mock_ptarpmir_predictions.tsv
    │       └── mock_gene_annotation.tsv
    ├── src/
    │   ├── normalize_predictions.py
    │   ├── build_consensus.py
    │   ├── generate_gene_lists.py
    │   ├── summarize_support.py
    │   └── run_demo.py
    ├── results/
    │   └── expected/
    └── docs/
        └── workflow.md

## Input Data

All input files are synthetic and stored in:

    data/mock/

The mock inputs simulate outputs from four miRNA target-prediction tools:

- miRanda
- RNAhybrid
- psRNATarget
- PTarPmiR

Every prediction file contains at least:

- `mirna_id`
- `target_id`

Tool-specific columns are preserved as an evidence field during normalization.

## Installation

Create and activate a Python environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

## Run the Demo

From the repository root:

    python src/run_demo.py

## Expected Outputs

The workflow generates:

    results/expected/normalized/all_predictions_long.tsv
    results/expected/consensus/mirna_target_consensus.tsv
    results/expected/gene_lists/
    results/expected/summary/tool_support_summary.tsv
    results/expected/summary/consensus_level_summary.tsv

## Consensus Logic

For each `mirna_id` and `target_id` pair:

- `tool_support_n` = number of prediction tools supporting the interaction;
- `tools_supporting` = semicolon-separated list of tools;
- `consensus_level`:
  - `high` = supported by 3 or more tools;
  - `medium` = supported by 2 tools;
  - `single_tool` = supported by 1 tool.

## Workflow Scripts

- `src/normalize_predictions.py`: converts heterogeneous mock prediction files into one standardized long-format table.
- `src/build_consensus.py`: groups predictions by miRNA-target pair and calculates consensus support.
- `src/generate_gene_lists.py`: exports one target-gene list per mock miRNA.
- `src/summarize_support.py`: generates summary tables by tool and consensus level.
- `src/run_demo.py`: runs the complete workflow in order.

## Limitations

This repository is a portfolio demonstration. It does not provide biological validation.

Important limitations:

- all data are synthetic/mock;
- scores are illustrative and not biologically meaningful;
- consensus support does not prove that a target is real;
- real miRNA target analysis requires careful tool selection, parameter control, reference versioning, biological interpretation, and experimental validation;
- this demo does not perform real target prediction or wet-lab validation.

## Author

Enrique A. Caban Centeno  
PhD researcher and bioinformatics analyst

Focus areas: RNA/miRNA analysis, sequence analysis, biological annotation, qPCR data processing, reproducible Python/R workflows, and omics-style data analysis.

## License

This project is released under the MIT License. See the LICENSE file for details.

## Portfolio Relevance

This repository was created as a public portfolio example for RNA/miRNA bioinformatics workflows. It demonstrates how heterogeneous prediction outputs can be standardized, integrated, summarized, and converted into consensus-based result tables using a reproducible Python workflow.

The project is suitable for demonstrating skills in Python, pandas, bioinformatics data processing, multi-tool result integration, target prioritization logic, and scientific workflow documentation.

A concise portfolio-oriented summary is available in:

    docs/portfolio_summary.md
