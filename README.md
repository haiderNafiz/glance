# Glance — AI Beauty Consultant

Glance is an AI-powered personalized beauty and hair consultant system designed to analyze visual traits, understand aesthetic preferences, and recommend tailored hair looks with evidence-backed provenance.

---

## Repository Structure

```
glance/
├── src/glance/
│   └── domain/
│       ├── contracts/          # Base, perception, intent, context, and recommendation contracts
│       ├── services/           # Service protocols and domain interfaces
│       └── taxonomy/           # Operational hair domain taxonomy (length, texture, volume, etc.)
├── tests/                      # Pytest suite for contracts, taxonomy, and services
├── docs/                       # Architectural specs and dataset provenance guides
└── data/                       # Dataset catalog (Git manifests + DVC-tracked binary images)
    ├── calibration/            # Iterative prompt & taxonomy calibration (v0.1, v0.2, v0.3)
    └── evaluation/             # Objective perception benchmark (v0.1 prepared)
```

---

## Datasets & DVC Tracking

Glance binary datasets (calibration images and evaluation benchmarks) are version-controlled via **DVC** and stored on **DagsHub Storage** (`https://dagshub.com/haiderNafiz/glance`).

### Pulling Datasets
```bash
dvc pull
```

For complete details on dataset architecture, provenance, and adding new versions, see [docs/DATASET_PROVENANCE.md](docs/DATASET_PROVENANCE.md).

---

## Development & Testing

### Running Unit Tests
```bash
pytest
```