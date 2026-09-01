# Glance Hair Perception Evaluation Datasets

## Purpose & Scope

Evaluation datasets serve as the **objective ground-truth benchmark** for evaluating the Glance Hair Perception System (`HairPerceptionService` and downstream look recommendation services).

Unlike calibration datasets (which are exploratory and used for prompt tuning), evaluation datasets:
1. Represent fixed, version-controlled test benchmarks.
2. Require rigorous ground truth annotations containing both **generation targets** and **human-verified observations**.
3. Evaluate model accuracy, category separability, and perception reliability across balanced demographic and viewpoint distributions.

---

## Evaluation Benchmark Versions

| Version | Status | Total Target | Description |
| :--- | :--- | :--- | :--- |
| **`v0.1`** | Infrastructure Prepared (Awaiting Generation) | 100 images | Standard 100-image evaluation benchmark covering all 7 taxonomy length categories, multiple textures, wave patterns, and viewpoints. |

---

## Metadata Governance & Schema Requirements

Future evaluation manifests must strictly distinguish between:
1. **`generation_target`**: The prompt intent and target attributes requested during synthetic image generation.
2. **`ground_truth_annotation`**: The independent, human-verified reality observed in the rendered image.
3. **`provenance`**: Generation seed, model checkpoint, pipeline config, and timestamp.
