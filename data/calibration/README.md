# Glance Hair Perception Calibration Datasets

## Purpose & Scope

The calibration datasets contained in this directory are **not** the final evaluation benchmark. Their sole purpose is iterative calibration of synthetic image generation prompts and validation of operational hair-length taxonomy categories for Glance MVP 1.

```
Generation Prompts
       ↓
Synthetic Calibration Images
       ↓
Human Inspection
       ↓
Taxonomy Separability Analysis
       ↓
Prompt & Taxonomy Refinement
       ↓
Accepted Calibration Version (v0.3)
       ↓
100-Image Evaluation Benchmark (v0.1)
```

---

## Calibration Dataset Versions

| Version | Status | Samples | Focus / Evolution Summary |
| :--- | :--- | :--- | :--- |
| **`v0.1`** | Historical / Immutable | 28 images | Initial taxonomy and prompt baseline calibration across 7 length categories. |
| **`v0.2`** | Historical / Immutable | 24 images | Introduced stronger anatomical and structural constraints in prompts. |
| **`v0.3`** | Accepted / Immutable | 21 images | Fine-tuned prompt guidance to maximize visual separation between problematic categories (`LONG` vs `VERY_LONG`). |

---

## Target Taxonomy Categories Calibrated

- `VERY_SHORT` (Above ear landmark)
- `SHORT` (Ear to jaw landmark)
- `BOB` (Chin / jaw level structure)
- `SHOULDER` (Shoulder level landmark)
- `MEDIUM` (Collarbone / upper chest region)
- `LONG` (Upper back to mid-back)
- `VERY_LONG` (Waist level or below)

---

## Version Preservation Policy

Every calibration iteration (`v0.1`, `v0.2`, `v0.3`) is strictly immutable. Images, generation parameters, random seeds, and metadata are permanently archived to guarantee full historical reproducibility.
