# Glance Hair Perception Calibration Dataset v0.1

Purpose:
Calibration of synthetic image generation prompts and operational
hair-length taxonomy for Glance MVP 1.

Dataset type:
Synthetic calibration dataset.

Model:
FLUX.2-klein-4B

Purpose of this dataset:
- Validate taxonomy separability
- Validate generation prompts
- Identify ambiguous hair-length categories
- Calibrate human annotation procedure

This is NOT the final evaluation dataset.

Target taxonomy categories:
- VERY_SHORT
- SHORT
- BOB
- SHOULDER
- MEDIUM
- LONG
- VERY_LONG

Viewpoint:
Viewpoint should be explicitly recorded in metadata.

The initial calibration set may contain rear-view images because
rear views make hair-length landmarks easier to inspect.
The final evaluation dataset should contain multiple viewpoints.

Human verification:
Each generated image should be manually reviewed against its
target taxonomy category before being accepted for evaluation.

Dataset version:
calibration-v0.1
