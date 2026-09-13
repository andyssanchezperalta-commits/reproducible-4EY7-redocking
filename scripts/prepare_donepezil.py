from __future__ import annotations

import argparse
from pathlib import Path

from rdkit import Chem


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Protonate the tertiary amine of crystallographic donepezil while preserving 3D coordinates.")
    p.add_argument("input_sdf", type=Path)
    p.add_argument("output_sdf", type=Path)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    suppl = Chem.SDMolSupplier(str(args.input_sdf), removeHs=False)
    mol = next((m for m in suppl if m is not None), None)
    if mol is None:
        raise ValueError("Could not read ligand SDF")

    rw = Chem.RWMol(mol)
    candidate_idx = None
    for atom in rw.GetAtoms():
        if atom.GetAtomicNum() == 7 and atom.GetFormalCharge() == 0 and atom.GetDegree() == 3:
            candidate_idx = atom.GetIdx()
            break

    if candidate_idx is None:
        raise ValueError("No neutral tertiary amine found")

    n = rw.GetAtomWithIdx(candidate_idx)
    n.SetFormalCharge(1)
    n.SetNoImplicit(False)
    protonated = rw.GetMol()
    Chem.SanitizeMol(protonated)
    protonated = Chem.AddHs(protonated, addCoords=True)

    writer = Chem.SDWriter(str(args.output_sdf))
    writer.write(protonated)
    writer.close()

    print(f"Wrote protonated ligand to {args.output_sdf}")
    print(f"Formal charge: {Chem.GetFormalCharge(protonated)}")
    print(f"Heavy atoms: {protonated.GetNumHeavyAtoms()}")


if __name__ == "__main__":
    main()
