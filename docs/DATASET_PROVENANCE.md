# Glance Dataset Provenance & DagsHub Integration Guide

This guide details the dataset version control architecture, provenance tracking standards, and DagsHub synchronization workflow for **Glance**.

---

## 1. Provenance Architecture

To guarantee 100% reproducibility of all experiments, evaluations, and perception benchmarks, Glance connects five dimensions of data lineage:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                PROVENANCE MATRIX                                │
├──────────────────────────┬──────────────────────────────────────────────────────┤
│ Lineage Dimension        │ Tracking Mechanism & Repository Location             │
├──────────────────────────┼──────────────────────────────────────────────────────┤
│ Taxonomy Definitions     │ Git commit (`src/glance/domain/taxonomy/hair.py`)    │
│ Prompt & Generation Meta │ Git-tracked JSON (`data/**/metadata/*.json`)         │
│ Random Seed & Checkpoint │ Manifest parameters (`seed`, `model`, `steps`)       │
│ Image Binary Blobs       │ DVC cryptographic content hash (`*.dvc` files)       │
│ Remote Storage & Web UI  │ DagsHub Storage (`https://dagshub.com/haiderNafiz/glance`) │
└──────────────────────────┴──────────────────────────────────────────────────────┘
```

---

## 2. DagsHub & DVC Connection

Glance uses DVC with DagsHub Storage as the centralized binary dataset remote.

### Remote Configuration
The public DVC remote endpoint is configured in `.dvc/config`:
```ini
[core]
    remote = origin
['remote "origin"']
    url = https://dagshub.com/haiderNafiz/glance.dvc
```

### Local Authentication
DVC authentication credentials are stored locally in `.dvc/config.local` (which is gitignored):
```bash
dvc remote modify origin --local auth basic
dvc remote modify origin --local user <DAGSHUB_USERNAME>
dvc remote modify origin --local password <DAGSHUB_TOKEN>
```

---

## 3. Dataset Lifecycle & Workflows

### Scenario A: Cloning Repository & Pulling Data
```bash
git clone https://github.com/haiderNafiz/glance.git
cd glance
dvc pull
```

### Scenario B: Adding a New Evaluation Dataset Version
1. Generate evaluation images into `data/evaluation/v0.1/images/`.
2. Populate `data/evaluation/v0.1/manifest.json` using `manifest_template.json`.
3. Add to DVC:
   ```bash
   dvc add data/evaluation/v0.1/images
   ```
4. Commit Git metadata & DVC pointers:
   ```bash
   git add data/evaluation/v0.1/images.dvc data/evaluation/v0.1/manifest.json data/evaluation/v0.1/README.md
   git commit -m "feat(data): add evaluation dataset v0.1 benchmark"
   git push origin main
   dvc push
   ```

---

## 4. Verification Standards
- **Binary Exclusion**: Ensure `.gitignore` prevents `.png`, `.jpg`, and binary directories from being staged in Git.
- **Hash Preservation**: Validate that dataset images match their expected SHA256 hashes before and after migration.
