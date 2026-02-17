---
name: scientific-computing
description: Use when "scientific computing", "astronomy", "astropy", "bioinformatics", "biopython", "symbolic math", "sympy", "statistics", "statsmodels", "scientific Python"
version: 1.0.0
---

# Scientific Computing

Domain-specific Python libraries for scientific applications.

## Libraries

| Library | Domain | Purpose |
|---------|--------|---------|
| **AstroPy** | Astronomy | Coordinates, units, FITS files |
| **BioPython** | Bioinformatics | Sequences, BLAST, PDB |
| **SymPy** | Mathematics | Symbolic computation |
| **Statsmodels** | Statistics | Statistical modeling, tests |

---

## AstroPy

Astronomy and astrophysics computations.

**Key capabilities:**

- **Units**: Physical unit handling with automatic conversion
- **Coordinates**: Celestial coordinate systems (ICRS, galactic, etc.)
- **Time**: Astronomical time scales (UTC, TAI, Julian dates)
- **FITS**: Read/write FITS astronomical data format

**Key concept**: Unit-aware calculations prevent errors from unit mismatches.

---

## BioPython

Bioinformatics - sequences, structures, databases.

**Key capabilities:**

- **Sequences**: DNA/RNA/protein manipulation, translation, complement
- **File parsing**: FASTA, GenBank, PDB formats
- **BLAST**: Local and remote sequence alignment
- **NCBI Entrez**: Database access (nucleotide, protein, taxonomy)

**Key concept**: `SeqIO` for reading any sequence format, `Seq` for sequence operations.

---

## SymPy

Symbolic mathematics - algebra, calculus, equation solving.

**Key capabilities:**

- **Algebra**: Solve equations, simplify, expand, factor
- **Calculus**: Derivatives, integrals, limits, series
- **Linear algebra**: Matrix operations, eigenvalues
- **Printing**: LaTeX output for documentation

**Key concept**: Work with symbols, not numbers. Get exact answers, not approximations.

---

## Statsmodels

Statistical modeling with R-like formula interface.

**Key capabilities:**

- **Regression**: OLS, logistic, generalized linear models
- **Time series**: ARIMA, VAR, state space models
- **Statistical tests**: t-tests, ANOVA, diagnostics
- **Formula API**: R-style formulas (`y ~ x1 + x2`)

**Key concept**: `model.summary()` gives comprehensive statistical output like R.

---

## Decision Guide

| Domain | Library |
|--------|---------|
| Astronomy/astrophysics | AstroPy |
| Biology/genetics | BioPython |
| Symbolic math | SymPy |
| Statistical analysis | Statsmodels |
| Numerical computing | NumPy, SciPy |
| Data manipulation | Pandas |

## Resources

- AstroPy: <https://docs.astropy.org>
- BioPython: <https://biopython.org/docs/>
- SymPy: <https://docs.sympy.org>
- Statsmodels: <https://www.statsmodels.org>
