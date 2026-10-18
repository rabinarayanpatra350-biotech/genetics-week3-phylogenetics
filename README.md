# Phylogenetic Analysis and Tree Reconstruction of COX1 Across Twelve Vertebrate Species

**Genetics Assistant Internship — Week 3** | Rabi Narayan Patra | 28 September 2026

A complete phylogenetic analysis of cytochrome c oxidase subunit 1 (COX1 / MT-CO1) — the mitochondrial gene that underpins DNA barcoding — across 12 vertebrate species, built from **publicly available sequences** with screening, alignment, distance estimation, tree reconstruction and bootstrap support.

## The dataset

Sequences were retrieved from **UniProt** (curated entries with explicit organism assignment) and **NCBI** (nucleotide COI barcodes, used for the screening case study):

| Species | Group | Accession | Length |
|---|---|---|---|
| Homo sapiens | mammal (primate) | P00395 | 513 aa |
| Pan troglodytes | mammal (primate) | Q9T9W1 | 513 aa |
| Mus musculus | mammal (rodent) | Q7JD04 | 514 aa |
| Bos taurus | mammal (artiodactyl) | P00396 | 514 aa |
| Canis lupus familiaris | mammal (carnivore) | Q9ZZ64 | 514 aa |
| Gallus gallus | bird | P18943 | 515 aa |
| Columba livia | bird | D4PBR3 | 516 aa |
| Anolis carolinensis | reptile | B3GSZ2 | 514 aa |
| Xenopus laevis | amphibian | P00398 | 519 aa |
| Danio rerio | ray-finned fish | A0A0A0VG02 | 516 aa |
| Salmo salar | ray-finned fish | Q9ZZM6 | 516 aa |
| Petromyzon marinus | jawless fish (outgroup) | Q35536 | 517 aa |

## Results at a glance

**Clades recovered with strong bootstrap support** (500 replicates, BLOSUM62 NJ):

| Clade | Support |
|---|---|
| *Homo sapiens* + *Pan troglodytes* (primates) | 100% |
| Mammals (5 species) | 94% |
| *Gallus gallus* + *Columba livia* (birds) | 100% |
| *Danio rerio* + *Salmo salar* (ray-finned fish) | 99% |

**Pairwise divergences match published values almost exactly** — the strongest evidence the data and alignment are sound:

| Pair | Observed identity | Expected |
|---|---|---|
| human – chimpanzee | 98.8% | ~99% |
| human – mouse | 90.8% | ~90% |
| cattle – dog | 96.9% | ~96% |
| human – chicken | 84.6% | ~84% |
| chicken – pigeon | 96.3% | ~96% |
| zebrafish – salmon | 95.0% | ~95% |

**The deepest nodes are NOT resolved — and the report says so.** None of seven amino-acid distance models recovers the amniote or tetrapod clade, and the reptile is misplaced outside the bird–mammal group (bootstrap 14%). Rather than hiding this, the report diagnoses the cause: long-branch attraction with sparse taxon sampling, single-gene data, and an anomalously conserved outgroup record.

## Two data-quality findings (both reported, not hidden)

1. **A mislabelled public record.** A GenBank entry submitted as *Gallus gallus* COX1 (PV636066.1) is **99.8% identical to human** — impossible for a bird (expected ~85%). It is a mislabelled or contaminated submission; it was detected by reference-identity screening, excluded, and replaced.
2. **An anomalously conserved outgroup.** The lamprey sequence is only 14.6% divergent from human where 20–22% is expected, which plausibly contributes to the instability at the deepest nodes.

Screening every record against a reference before alignment is therefore treated as a **required step**, not an optional one.

## Repository contents

```
├── README.md
├── scripts/
│   └── 00_fetch_uniprot.py        # sequence retrieval (UniProt REST, length-disambiguated)
└── results/
    ├── bootstrap_support.csv      # clade support (500 replicates)
    ├── model_comparison.csv       # clade recovery across 7 amino-acid models
    └── taxonomic_congruence.csv   # recovered vs expected clades
```

The complete project — all four scripts (`00_fetch_uniprot.py`, `01_phylogeny.py`, `02_make_figures.py`, `03_build_report.py`), the retrieved sequences with provenance, the 521-column alignment, every distance matrix, the tree files, all eight figures and the report — is attached to the [v1.0 release](https://github.com/rabinarayanpatra350-biotech/genetics-week3-phylogenetics/releases/tag/v1.0) as a reproducibility bundle.

## Methods in brief

**Screening** (length, ambiguous residues, identity vs a verified reference) → **alignment** (FAMSA; reference-anchored projection for nucleotide fragments) → **distances** (p-distance; Poisson correction d = −ln(1−p); Kimura 2-parameter for nucleotides; BLOSUM62 for tree building) → **trees** (Neighbour-Joining, UPGMA for comparison) → **support** (500 bootstrap replicates by column resampling) → **diagnostics** (saturation, seven-model robustness comparison, molecular-clock root-to-tip check).

## Author

**Rabi Narayan Patra** — Genetics Assistant Internship (2026). GitHub: [@rabinarayanpatra350-biotech](https://github.com/rabinarayanpatra350-biotech)
