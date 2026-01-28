---
name: lammps-simulation
description: Run LAMMPS molecular dynamics simulations. Use when asked to run MD simulations, energy minimization, equilibration, production runs, or calculate properties like diffusion, RDF, MSD. Supports both CPU and GPU execution.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# LAMMPS Molecular Dynamics Simulation

You are executing LAMMPS molecular dynamics simulations on this workstation.

## CRITICAL: Finding Your Own Parameters

**You must find force field parameters yourself. They are NOT provided.**

### How to Find Force Field Parameters

**Step 1: Identify what you need**
- What material? (argon, water, copper, etc.)
- What property? (diffusion, structure, thermal conductivity)
- What conditions? (temperature, pressure)

**Step 2: Search literature**
```
Good search queries:
- "[material] lennard-jones parameters molecular dynamics"
- "[material] force field molecular dynamics"
- "[material] interatomic potential parameters"
- "[water model] parameters" (for TIP3P, TIP4P, SPC/E, etc.)
- "[metal] EAM potential"
```

**Step 3: Find authoritative sources**

| Material | Seminal Paper | Key Values |
|----------|--------------|------------|
| Liquid Argon | Rahman 1964, Phys. Rev. 136, A405 | ε/kB=119.8 K, σ=3.405 Å |
| TIP4P Water | Jorgensen 1983, J. Chem. Phys. 79, 926 | See paper Table I |
| TIP3P Water | Jorgensen 1983 (same paper) | ε=0.1521 kcal/mol, σ=3.1507 Å |
| SPC/E Water | Berendsen 1987, J. Phys. Chem. 91, 6269 | qO=-0.8476e, ε=0.1553 kcal/mol |

**Step 4: Download supplementary materials if needed**
Use Playwright or WebFetch to get SI with parameter tables.

**Step 5: Convert units**
```
kJ/mol → kcal/mol: divide by 4.184
eV → kcal/mol: multiply by 23.06
K → kcal/mol: multiply by 0.001987 (kB)
```

**Step 6: Document source in input file**
```lammps
# Lennard-Jones parameters for liquid argon
# Source: Rahman, Phys. Rev. 136, A405 (1964)
# ε/kB = 119.8 K = 0.238 kcal/mol, σ = 3.405 Å
pair_coeff 1 1 0.238 3.405
```

---

## Binary Location

LAMMPS is configured via environment variable (set in `.claude/settings.json` or shell):

```bash
# From environment variable
LMP="${LMP:-lmp}"  # Falls back to 'lmp' in PATH

# Or check your config
echo $LMP
```

### Execution Commands

**CPU:**
```bash
$LMP -in input.lmp
```

**GPU (for large systems):**
```bash
$LMP -sf gpu -pk gpu 1 neigh yes -in input.lmp
```

---

## Complete Workflow (Agentic)

### Example: Liquid Argon Diffusion

**Given only:** "Calculate the self-diffusion coefficient of liquid argon"

**You do:**

1. **Search literature** for argon MD parameters
   - Find Rahman 1964 as seminal paper
   - Extract: ε/kB = 119.8 K, σ = 3.405 Å
   - Note conditions: T = 94.4 K (triple point), ρ = 1.374 g/cm³

2. **Convert parameters**
   - ε = 119.8 K × 0.001987 kcal/(mol·K) = 0.238 kcal/mol

3. **Calculate system size**
   - N = 864 atoms (Rahman's choice, or 256-500 for faster)
   - Box size from density: L = (N × M / (ρ × Nₐ))^(1/3)

4. **Create input file with citations**
   ```lammps
   # Liquid Argon MD - Self-diffusion calculation
   # Parameters from Rahman, Phys. Rev. 136, A405 (1964)

   units           real
   atom_style      atomic
   boundary        p p p

   # Create FCC lattice, will melt to liquid
   lattice         fcc 5.26   # ~1.374 g/cm³
   region          box block 0 6 0 6 0 6
   create_box      1 box
   create_atoms    1 box
   mass            1 39.948   # Argon

   # LJ potential - Rahman 1964 parameters
   pair_style      lj/cut 10.0
   pair_coeff      1 1 0.238 3.405  # ε=0.238 kcal/mol, σ=3.405 Å

   # Initialize velocities at target temperature
   velocity        all create 94.4 12345

   # Equilibration
   fix             1 all nvt temp 94.4 94.4 100.0
   timestep        2.0
   thermo          100
   run             10000

   # Production with trajectory for MSD
   reset_timestep  0
   dump            1 all custom 100 trajectory.lammpstrj id type x y z
   run             50000
   ```

5. **Run simulation**
   ```bash
   $LMP -in input.lmp
   ```

6. **Analyze MSD and extract D**
   - Use LAMMPS compute msd or post-process trajectory
   - D = lim(t→∞) MSD(t) / (6t)

7. **Compare to literature**
   - Rahman 1964: D ≈ 2.43 × 10⁻⁵ cm²/s
   - Your result should be within ~10%

---

## Common Pair Styles and When to Use

| Pair Style | Use For | Notes |
|------------|---------|-------|
| `lj/cut` | Noble gases, simple fluids | Need ε, σ from literature |
| `lj/cut/coul/long` | Molecular systems with charges | Combine with kspace |
| `eam` | Metals | Download .eam file from literature |
| `tersoff` | Covalent (Si, C, etc.) | Use published parameter files |
| `reaxff` | Reactive systems | Requires force field file |

### Finding EAM Potentials for Metals

1. Search: "[metal] EAM potential LAMMPS"
2. Check NIST Interatomic Potentials Repository: https://www.ctcms.nist.gov/potentials/
3. Download the .eam.alloy or .eam.fs file
4. Reference in input:
   ```lammps
   pair_style eam/alloy
   pair_coeff * * Cu_Zhou04.eam.alloy Cu
   ```

---

## Input File Structure

1. **Units and style** - `units real` for most molecular systems
2. **Structure** - `read_data` or create with `lattice`/`create_atoms`
3. **Force field** - `pair_style` and `pair_coeff` (YOU FIND THESE)
4. **Dynamics** - `fix nvt/npt/nve`, `timestep`
5. **Output** - `thermo`, `dump`
6. **Run** - `minimize` or `run`

---

## Common Issues and Solutions

1. **"Unknown pair style"** - Style not compiled in. Check `$LMP -h` for available.
2. **"Bond atom missing"** - Topology error in data file
3. **"Out of range atoms"** - Timestep too large or bad parameters
4. **Wrong temperature/energy** - Check unit consistency (real vs metal vs lj)

---

## Property Calculations

### Diffusion Coefficient
```lammps
compute         msd all msd
fix             msd_out all ave/time 100 1 100 c_msd[4] file msd.dat
```
Then: D = slope(MSD vs t) / 6

### Radial Distribution Function
```lammps
compute         rdf all rdf 100
fix             rdf_out all ave/time 100 1 100 c_rdf[*] file rdf.dat mode vector
```

### Temperature/Pressure
Already in thermo output by default.

---

## Key Principle

**Don't use placeholder parameters.** Every `pair_coeff` line should have a citation in the comments. If you can't find parameters, search harder or report that the parameters aren't available in literature.
