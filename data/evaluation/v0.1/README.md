# Glance Hair Perception Evaluation Benchmark v0.1

## Overview
- **Benchmark Version**: `evaluation-v0.1`
- **Target Sample Count**: 100 images
- **Status**: Infrastructure Prepared (Pending synthetic generation following calibration acceptance)

## Dataset Structure
```
data/evaluation/v0.1/
├── README.md                  # This specification document
├── manifest_template.json     # Structure definition for sample annotations
├── manifest.json              # [To be generated] 100 ground-truth annotated samples
├── images.dvc                 # [To be generated] DVC tracking pointer
└── images/                    # [DVC Tracked] 100 evaluation PNG images
```

## Category Distribution Target (100 Samples)
- `VERY_SHORT`: ~14 samples
- `SHORT`: ~14 samples
- `BOB`: ~14 samples
- `SHOULDER`: ~15 samples
- `MEDIUM`: ~15 samples
- `LONG`: ~14 samples
- `VERY_LONG`: ~14 samples

## Verification Protocol
Each generated image in this evaluation set must undergo human verification against its target taxonomy category. The ground-truth metadata records whether the synthetic generation matched the target prompt or required human adjustment.
