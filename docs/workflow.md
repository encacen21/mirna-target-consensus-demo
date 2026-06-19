# Workflow Notes

This document describes the logic of the synthetic miRNA target-consensus demo.

## Goal

The goal is to demonstrate how outputs from multiple miRNA target-prediction tools can be normalized and integrated into a consensus table.

This is a public portfolio demo. It uses only synthetic data.

## Workflow Steps

1. Read mock prediction files from several tools.
2. Normalize all predictions into one long-format table.
3. Group predictions by `mirna_id` and `target_id`.
4. Count the number of tools supporting each interaction.
5. Store the supporting tool names.
6. Assign a simple consensus level.
7. Join mock gene annotations.
8. Export consensus tables, gene lists, and summary tables.

## Input Requirements

Each prediction file must contain at least:

- `mirna_id`
- `target_id`

Additional columns are treated as tool-specific evidence.

## Consensus Levels

- `high`: interaction supported by three or more tools.
- `medium`: interaction supported by two tools.
- `single_tool`: interaction supported by one tool.

## Output Files

The main output is:

    results/expected/consensus/mirna_target_consensus.tsv

Additional outputs include normalized predictions, gene lists by miRNA, and summary tables.

## Safety Note

This repository must remain free of real thesis data, real candidate genes, real organisms from unpublished projects, private paths, logs, credentials, reports, or unpublished results.
