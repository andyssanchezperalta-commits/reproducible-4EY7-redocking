# Reproducible 4EY7 Redocking

A reproducible molecular redocking workflow for **donepezil** in **human acetylcholinesterase (AChE)** using the crystallographic complex **PDB 4EY7**. The workflow covers receptor/ligand extraction, ligand preparation, AutoDock Vina docking, pose validation by RMSD, and multi-seed reproducibility analysis.

## Objective

The goal of this project is to test whether a docking workflow can recover the experimentally observed binding pose of the co-crystallized ligand. Redocking is used here as a **workflow validation benchmark**: the crystallographic ligand is removed, docked back into the binding site, and the predicted pose is compared with the experimental pose.

## Workflow

1. Download the 4EY7 structure from the RCSB Protein Data Bank.
2. Extract chain A receptor atoms and the crystallographic donepezil ligand (residue `E20`, chain A, residue 604).
3. Prepare the receptor with Meeko.
4. Prepare the ligand with RDKit/Meeko using the protonated tertiary amine state used in this workflow.
5. Define a 20 × 20 × 20 Å docking box centered on the crystallographic ligand.
6. Run AutoDock Vina with `exhaustiveness = 32`, `num_modes = 20`, and multiple random seeds.
7. Export docking poses and calculate symmetry-aware heavy-atom RMSD against the crystallographic pose.
8. Compare results across seeds to assess pose-recovery reproducibility.

## Docking box

- Center: **(-14.108, -43.833, 27.670) Å**
- Size: **20 × 20 × 20 Å**

See [`config/vina_box.txt`](config/vina_box.txt).

## Main result

For the initial run (`seed = 20260912`):

- Best Vina score: **-12.178 kcal/mol**
- Heavy-atom RMSD of the top-ranked pose: **0.374 Å**

Across five independent seeds:

| Seed | Best Vina score (kcal/mol) | Top-pose RMSD (Å) |
|---:|---:|---:|
| 20260912 | -12.178 | 0.374 |
| 20260913 | -12.183 | 0.336 |
| 20260914 | -12.196 | 0.342 |
| 20260915 | -12.178 | 0.385 |
| 20260916 | -12.179 | 0.380 |

Mean top-pose RMSD: **0.364 Å**  
Mean best Vina score: **-12.183 kcal/mol**  
Runs with top-pose RMSD ≤ 2 Å: **5/5**

The conventional ≤2 Å pose-recovery criterion is included only as a practical redocking heuristic. A Vina score is a scoring-function estimate and should not be interpreted as an experimental binding free energy or exact affinity.

## Repository structure

```text
.
├── README.md
├── environment.yml
├── config/
│   └── vina_box.txt
├── scripts/
│   ├── extract_4ey7.py
│   ├── prepare_donepezil.py
│   ├── calculate_rmsd.py
│   └── summarize_reproducibility.py
└── results/
    └── multi_seed_results.csv
```

Raw PDB/SDF files and generated docking outputs are intentionally not tracked here. They can be downloaded/generated from the original public structure and the scripts in this repository.

## Environment

The workflow was developed on Windows with Python 3.11. A minimal Conda environment is provided in [`environment.yml`](environment.yml).

```bash
conda env create -f environment.yml
conda activate neurodock
```

AutoDock Vina 1.2.7 is used as an external executable.

## Example receptor and ligand extraction

```bash
python scripts/extract_4ey7.py 4EY7.pdb --outdir prepared
```

## Example Vina run

After preparing receptor and ligand PDBQT files with Meeko:

```bash
vina \
  --receptor prepared/4EY7_receptor.pdbqt \
  --ligand prepared/4EY7_donepezil.pdbqt \
  --center_x -14.108 --center_y -43.833 --center_z 27.670 \
  --size_x 20 --size_y 20 --size_z 20 \
  --exhaustiveness 32 \
  --num_modes 20 \
  --energy_range 5 \
  --seed 20260912 \
  --out docking/docked_seed_20260912.pdbqt
```

## RMSD validation

The RMSD script compares heavy atoms in docked SDF poses with the crystallographic reference using RDKit's symmetry-aware atom mapping without pre-aligning the coordinates.

```bash
python scripts/calculate_rmsd.py \
  --reference prepared/4EY7_donepezil_protonated.sdf \
  --poses docking/docked_seed_20260912.sdf
```

## Reproducibility summary

```bash
python scripts/summarize_reproducibility.py results/multi_seed_results.csv
```

## Scientific scope

This repository demonstrates **pose-recovery reproducibility for one crystallographic complex**. It does not by itself establish general docking accuracy across targets, experimental binding affinity, clinical efficacy, or pharmacological response.

## Data source

- RCSB PDB: [4EY7](https://www.rcsb.org/structure/4EY7)

## Tools

- Python 3.11
- RDKit
- Meeko 0.8.0
- AutoDock Vina 1.2.7
- ChimeraX
- NumPy / pandas

---

Created as part of an independent computational biology learning project focused on reproducible molecular docking and validation.