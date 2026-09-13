from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Extract chain A receptor and crystallographic donepezil (E20 A 604) from PDB 4EY7.")
    p.add_argument("pdb", type=Path, help="Input 4EY7 PDB file")
    p.add_argument("--outdir", type=Path, default=Path("prepared"))
    return p.parse_args()


def main() -> None:
    args = parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    receptor_lines: list[str] = []
    ligand_lines: list[str] = []

    with args.pdb.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            record = line[:6].strip()
            if record not in {"ATOM", "HETATM"}:
                continue

            chain = line[21:22]
            resname = line[17:20].strip()
            try:
                resseq = int(line[22:26])
            except ValueError:
                continue

            if record == "ATOM" and chain == "A":
                receptor_lines.append(line)
            elif record == "HETATM" and chain == "A" and resname == "E20" and resseq == 604:
                ligand_lines.append(line)

    receptor_path = args.outdir / "4EY7_A_receptor.pdb"
    ligand_path = args.outdir / "4EY7_donepezil_exp.pdb"

    receptor_path.write_text("".join(receptor_lines) + "END\n", encoding="utf-8")
    ligand_path.write_text("".join(ligand_lines) + "END\n", encoding="utf-8")

    print(f"Receptor atoms: {len(receptor_lines)}")
    print(f"Ligand heavy atoms: {len(ligand_lines)}")
    print(f"Wrote: {receptor_path}")
    print(f"Wrote: {ligand_path}")


if __name__ == "__main__":
    main()
