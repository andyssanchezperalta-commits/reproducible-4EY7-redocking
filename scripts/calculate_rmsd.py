from __future__ import annotations

import argparse
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import rdMolAlign


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Calculate symmetry-aware heavy-atom RMSD for docked poses against a reference ligand.")
    p.add_argument("--reference", required=True, type=Path)
    p.add_argument("--poses", required=True, type=Path)
    return p.parse_args()


def load_first_sdf(path: Path) -> Chem.Mol:
    suppl = Chem.SDMolSupplier(str(path), removeHs=False)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        raise ValueError(f"Could not read {path}")
    return mol


def heavy_only(mol: Chem.Mol) -> Chem.Mol:
    return Chem.RemoveHs(mol)


def main() -> None:
    args = parse_args()
    ref = heavy_only(load_first_sdf(args.reference))
    poses = Chem.SDMolSupplier(str(args.poses), removeHs=False)

    print("pose,rmsd_A")
    for i, pose in enumerate(poses, start=1):
        if pose is None:
            continue
        pose = heavy_only(pose)
        rmsd = rdMolAlign.CalcRMS(pose, ref)
        print(f"{i},{rmsd:.3f}")


if __name__ == "__main__":
    main()
