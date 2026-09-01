# Glance Dataset Registry & Versioning

This directory contains the dataset catalog and versioning records for **Glance AI Beauty Consultant** (MVP 1 — Personal Hair Look Explorer).

---

## Directory Architecture

```
data/
├── calibration/        # Iterative taxonomy & prompt calibration datasets (v0.1, v0.2, v0.3)
│   ├── v0.1/           # Initial taxonomy & prompt calibration
│   ├── v0.2/           # Structural constraints & prompt strategy refinement
│   └── v0.3/           # Refinement for fine category separability (LONG vs VERY_LONG)
└── evaluation/         # Objective system evaluation benchmarks
    └── v0.1/           # Upcoming 100-image evaluation benchmark (manifest template prepared)
```

---

## Storage & Tracking Strategy

| Component | Storage Location | Tracking Tool | Description |
| :--- | :--- | :--- | :--- |
| **Source Code & Manifests** | GitHub (`haiderNafiz/glance`) | Git | Pydantic contracts, prompt templates, JSON manifests, markdown documentation |
| **Pointer Files (`*.dvc`)** | GitHub (`haiderNafiz/glance`) | Git | Lightweight cryptographic pointer files pointing to image blobs |
| **Binary Image Datasets** | DagsHub Storage (`haiderNafiz/glance`) | DVC | High-resolution PNG image binaries and contact sheets |

---

## Developer Quickstart

### Pulling Datasets Locally
To download the binary image datasets from DagsHub DVC remote:
```bash
dvc pull
```

### Pulling Specific Versions
To pull a specific calibration version:
```bash
dvc pull data/calibration/v0.3/images.dvc
```

### Adding New Datasets
When introducing new calibration or evaluation dataset iterations:
1. Place image binaries in `data/<type>/vX.Y/images/`
2. Place text manifests and metadata in `data/<type>/vX.Y/metadata/` or `manifest.json`
3. Track binaries with DVC:
   ```bash
   dvc add data/<type>/vX.Y/images
   ```
4. Commit pointer files and metadata to Git:
   ```bash
   git add data/<type>/vX.Y/images.dvc data/<type>/vX.Y/*.json data/<type>/vX.Y/*.md
   git commit -m "feat(data): add <type> dataset vX.Y"
   ```
5. Push to remotes:
   ```bash
   git push origin main
   dvc push
   ```
