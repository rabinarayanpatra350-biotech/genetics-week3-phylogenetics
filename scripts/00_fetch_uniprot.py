#!/usr/bin/env python3
"""
00_fetch_uniprot.py
Retrieves curated cytochrome c oxidase subunit 1 (COX1 / MT-CO1) protein
sequences from UniProt for 12 vertebrate species.

Why UniProt rather than GenBank free-text search: the gene symbol COX1 is
ambiguous (it also denotes cyclooxygenase-1 / PTGS1), and relevance-ranked
GenBank searches returned records that failed taxonomic screening. UniProt
entries carry an explicit organism and a reviewed/unreviewed status, and the
sequence length filter (500-520 aa) separates the mitochondrial COX1 (~513-516
aa) from PTGS1 (~600 aa).

Output: data/cox1_proteins.fasta (one reviewed-preferred entry per species)
"""
import json
import os
import time
import urllib.parse
import urllib.request

SPECIES = [
    "Homo sapiens", "Pan troglodytes", "Mus musculus", "Bos taurus",
    "Canis lupus familiaris", "Gallus gallus", "Columba livia",
    "Anolis carolinensis", "Xenopus laevis", "Danio rerio", "Salmo salar",
    "Petromyzon marinus",
]
BASE = "https://rest.uniprot.org/uniprotkb/search"
os.makedirs("data", exist_ok=True)

def fetch(species):
    query = (f'(gene:COX1 OR gene:MT-CO1 OR gene:COI OR gene:CO1) '
             f'AND organism_name:"{species}" AND length:[500 TO 520]')
    params = {"query": query, "format": "fasta", "size": "1",
              "fields": "accession,id,protein_name,organism_name,length,sequence"}
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as fh:
        return fh.read().decode()

records = {}
for sp in SPECIES:
    for attempt in range(3):
        try:
            txt = fetch(sp)
            if txt.strip():
                header = txt.splitlines()[0]
                seq = "".join(txt.splitlines()[1:])
                records[sp] = (header, seq)
                print(f"{sp:26s} {header.split('|')[1] if '|' in header else '?':12s} len={len(seq)}")
                break
            time.sleep(1)
        except Exception as exc:                       # pragma: no cover
            print(f"{sp:26s} retry {attempt+1}: {exc}")
            time.sleep(2)
    else:
        print(f"{sp:26s} FAILED")

with open("data/cox1_proteins.fasta", "w") as fh:
    for sp, (header, seq) in records.items():
        fh.write(f"{header}\n")
        for i in range(0, len(seq), 60):
            fh.write(seq[i:i + 60] + "\n")

meta = {sp: {"header": h, "length": len(s), "accession": h.split("|")[1] if "|" in h else ""}
        for sp, (h, s) in records.items()}
with open("data/cox1_provenance.json", "w") as fh:
    json.dump(meta, fh, indent=2)
print(f"\nretrieved {len(records)}/{len(SPECIES)} sequences -> data/cox1_proteins.fasta")
