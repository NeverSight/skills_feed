---
name: package-npm-nix
description: Package npm/TypeScript/Bun CLI tools for Nix. Use when creating Nix derivations for JavaScript/TypeScript tools from npm registry or GitHub sources, handling pre-built packages or source builds with dependency management.
---

<objective>
Create Nix packages for npm-based CLI tools, covering both pre-built packages from npm registry and source builds with proper dependency management. This skill provides patterns for fetching, building, and packaging JavaScript/TypeScript/Bun tools in Nix environments.
</objective>

<quick_start>
<pre_built_from_npm>
For tools already built and published to npm (fastest approach):

```nix
{
  lib,
  stdenv,
  fetchzip,
  nodejs,
}:

stdenv.mkDerivation rec {
  pname = "tool-name";
  version = "1.0.0";

  src = fetchzip {
    url = "https://registry.npmjs.org/${pname}/-/${pname}-${version}.tgz";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
  };

  nativeBuildInputs = [ nodejs ];

  installPhase = ''
    runHook preInstall

    mkdir -p $out/bin
    cp $src/dist/cli.js $out/bin/tool-name
    chmod +x $out/bin/tool-name

    # Fix shebang
    substituteInPlace $out/bin/tool-name \
      --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node"

    runHook postInstall
  '';

  meta = with lib; {
    description = "Tool description";
    homepage = "https://github.com/org/repo";
    license = licenses.mit;
    sourceProvenance = with lib.sourceTypes; [ binaryBytecode ];
    maintainers = with maintainers; [ ];
    mainProgram = "tool-name";
    platforms = platforms.all;
  };
}
```

Get the hash:
```bash
nix-prefetch-url --unpack https://registry.npmjs.org/tool-name/-/tool-name-1.0.0.tgz
# Convert to SRI format:
nix hash convert --to sri --hash-algo sha256 <hash-output>
```
</pre_built_from_npm>

<source_build_with_bun>
For tools that need to be built from source using Bun:

```nix
{
  lib,
  stdenv,
  stdenvNoCC,
  fetchFromGitHub,
  bun,
  makeBinaryWrapper,
  nodejs,
  autoPatchelfHook,
}:

let
  fetchBunDeps =
    { src, hash, ... }@args:
    stdenvNoCC.mkDerivation {
      pname = args.pname or "${src.name or "source"}-bun-deps";
      version = args.version or src.version or "unknown";
      inherit src;

      nativeBuildInputs = [ bun ];

      buildPhase = ''
        export HOME=$TMPDIR
        export npm_config_ignore_scripts=true
        bun install --no-progress --frozen-lockfile --ignore-scripts
      '';

      installPhase = ''
        mkdir -p $out
        cp -R ./node_modules $out
        cp ./bun.lock $out/
      '';

      dontFixup = true;
      outputHash = hash;
      outputHashAlgo = "sha256";
      outputHashMode = "recursive";
    };

  version = "1.0.0";
  src = fetchFromGitHub {
    owner = "org";
    repo = "repo";
    rev = "v${version}";
    hash = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
  };

  node_modules = fetchBunDeps {
    pname = "tool-name-bun-deps";
    inherit version src;
    hash = "sha256-BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB=";
  };
in
stdenv.mkDerivation rec {
  pname = "tool-name";
  inherit version src;

  nativeBuildInputs = [
    bun
    nodejs
    makeBinaryWrapper
    autoPatchelfHook
  ];

  buildInputs = [
    stdenv.cc.cc.lib
  ];

  buildPhase = ''
    # Verify lockfile match
    diff -q ./bun.lock ${node_modules}/bun.lock || exit 1

    # Copy and patch node_modules
    cp -R ${node_modules}/node_modules .
    chmod -R u+w node_modules
    patchShebangs node_modules
    autoPatchelf node_modules

    export HOME=$TMPDIR
    export npm_config_ignore_scripts=true
    bun run build
  '';

  installPhase = ''
    mkdir -p $out/bin
    cp dist/tool-name $out/bin/tool-name
    chmod +x $out/bin/tool-name
  '';

  dontStrip = true;

  meta = with lib; {
    description = "Tool description";
    homepage = "https://github.com/org/repo";
    license = licenses.mit;
    sourceProvenance = with lib.sourceTypes; [ fromSource ];
    maintainers = with maintainers; [ ];
    mainProgram = "tool-name";
    platforms = [ "x86_64-linux" ];
  };
}
```
</source_build_with_bun>
</quick_start>

<workflow>
<step_1_identify_package_type>
**Determine build approach**:

Check the npm package:
```bash
# Download and inspect
nix-prefetch-url --unpack https://registry.npmjs.org/package/-/package-1.0.0.tgz
ls -la /nix/store/<hash>-package-1.0.0.tgz/
```

If `dist/` directory exists with built files:
→ Use pre-built approach (simpler, faster)

If only `src/` exists or package.json has build scripts:
→ Use source build approach

Check package.json for:
- `"bin"` field: Shows what executables are provided
- `"type": "module"`: ES modules (common in modern packages)
- `"scripts"`: Build commands (indicates source build needed)
- Runtime: Look for bun, node, or specific version requirements
</step_1_identify_package_type>

<step_2_fetch_hashes>
**Get source and dependency hashes**:

For pre-built packages:
```bash
# Fetch npm tarball
nix-prefetch-url --unpack https://registry.npmjs.org/pkg/-/pkg-1.0.0.tgz
# Output: 1abc... (base32 format)

# Convert to SRI format
nix hash convert --to sri --hash-algo sha256 1abc...
# Output: sha256-xyz...
```

For source builds:
```bash
# Get GitHub source hash
nix-prefetch-url --unpack https://github.com/org/repo/archive/v1.0.0.tar.gz

# Get dependencies hash (requires iteration):
# 1. Use lib.fakeHash in fetchBunDeps
# 2. Try to build
# 3. Nix will show expected hash in error
# 4. Update hash and rebuild
```
</step_2_fetch_hashes>

<step_3_create_package_files>
**Create package structure**:

```bash
mkdir -p packages/tool-name
```

Create `packages/tool-name/package.nix` with full derivation (see quick_start).

Create `packages/tool-name/default.nix`:
```nix
{ pkgs }: pkgs.callPackage ./package.nix { }
```

This two-file pattern allows the package to be used standalone or integrated into a flake.
</step_3_create_package_files>

<step_4_handle_special_cases>
**Common additional requirements**:

**WASM files or other assets**:
```nix
installPhase = ''
  mkdir -p $out/bin
  cp $src/dist/cli.js $out/bin/tool
  cp $src/dist/*.wasm $out/bin/  # Copy WASM alongside
  chmod +x $out/bin/tool

  substituteInPlace $out/bin/tool \
    --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node"
'';
```

**Multiple executables**:
```nix
# package.json might have:
# "bin": {
#   "tool": "dist/cli.js",
#   "tool-admin": "dist/admin.js"
# }

installPhase = ''
  mkdir -p $out/bin
  for exe in tool tool-admin; do
    cp $src/dist/$exe.js $out/bin/$exe
    chmod +x $out/bin/$exe
    substituteInPlace $out/bin/$exe \
      --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node"
  done
'';

meta.mainProgram = "tool";  # Primary command
```

**Platform-specific binaries**:
```nix
meta = {
  platforms = [ "x86_64-linux" ];  # Bun-compiled binaries often Linux-only
  # or
  platforms = platforms.all;  # Pure JS works everywhere
};
```
</step_4_handle_special_cases>

<step_5_test_build>
**Build and test**:

```bash
# Build
nix build .#tool-name

# Test the binary
./result/bin/tool-name --version
./result/bin/tool-name --help

# Check dependencies (Linux)
ldd ./result/bin/tool-name  # Should show all deps resolved

# Format
nix fmt

# Run flake checks
nix flake check
```
</step_5_test_build>
</workflow>

<metadata_requirements>
<essential_fields>
Every package must have complete metadata:

```nix
meta = with lib; {
  description = "Clear, concise description";
  homepage = "https://project-homepage.com";
  changelog = "https://github.com/org/repo/releases";  # Optional but nice
  license = licenses.mit;  # or licenses.unfree for proprietary
  sourceProvenance = with lib.sourceTypes; [
    fromSource          # Built from source
    # or
    binaryBytecode      # Pre-built JS/TS (npm dist/)
    # or
    binaryNativeCode    # Compiled binaries
  ];
  maintainers = with maintainers; [ ];  # Empty OK for community packages
  mainProgram = "binary-name";
  platforms = platforms.all;  # or specific: [ "x86_64-linux" ]
};
```
</essential_fields>

<source_provenance_guide>
**Choose based on what you're packaging**:

- `fromSource`: Built from TypeScript/source during derivation
- `binaryBytecode`: Pre-compiled JS from npm registry
- `binaryNativeCode`: Native binaries (Rust, Go, Bun-compiled)

This affects security auditing and reproducibility expectations.
</source_provenance_guide>
</metadata_requirements>

<common_patterns>
<shebang_replacement>
**Always replace shebangs** for reproducibility:

```nix
# Single file
substituteInPlace $out/bin/tool \
  --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node"

# Multiple files
find $out/bin -type f -exec substituteInPlace {} \
  --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node" \;
```

The `--replace-quiet` flag suppresses warnings if pattern not found.
</shebang_replacement>

<native_dependencies>
**Handle native modules** (like sqlite, sharp):

```nix
nativeBuildInputs = [
  bun
  nodejs
  makeBinaryWrapper
  autoPatchelfHook  # Linux: patches ELF binaries
];

buildInputs = [
  stdenv.cc.cc.lib  # Provides libgcc_s.so.1, libstdc++.so.6
];

autoPatchelfIgnoreMissingDeps = [
  "libc.musl-x86_64.so.1"  # Ignore musl if not available
];
```

`autoPatchelf` runs automatically on Linux, fixing RPATH for .so files.
</native_dependencies>

<bun_compiled_binaries>
**Don't strip Bun-compiled executables**:

```nix
# Bun embeds JavaScript in the binary
dontStrip = true;
```

Stripping would remove the embedded JS, breaking the program.
</bun_compiled_binaries>

<checking_tarball_contents>
**Inspect npm package structure**:

```bash
# After nix-prefetch-url
ls -la /nix/store/*-pkg-1.0.0.tgz/

# Common layouts:
# dist/cli.js          → Pre-built, use directly
# dist/index.js        → Main entry, check package.json "bin"
# src/index.ts         → Source only, need to build
# lib/                 → Built CommonJS
# esm/                 → Built ES modules
```

Check package.json to find the correct entry point.
</checking_tarball_contents>
</common_patterns>

<anti_patterns>
<avoid_these>
**Don't do this**:

❌ Hardcode node paths:
```nix
# Bad
"#!/usr/bin/node"  # Won't work on NixOS
```

✅ Use substituteInPlace:
```nix
# Good
substituteInPlace $out/bin/tool \
  --replace-quiet "#!/usr/bin/env node" "#!${nodejs}/bin/node"
```

❌ Skip hash verification:
```nix
# Bad - insecure
hash = lib.fakeHash;
```

✅ Get real hash:
```nix
# Good - reproducible and secure
hash = "sha256-actual-hash-here";
```

❌ Forget to make executable:
```nix
# Bad - won't run
cp $src/dist/cli.js $out/bin/tool
```

✅ Set executable bit:
```nix
# Good
cp $src/dist/cli.js $out/bin/tool
chmod +x $out/bin/tool
```

❌ Strip Bun binaries:
```nix
# Bad - breaks Bun-compiled executables
# (default behavior strips binaries)
```

✅ Disable stripping:
```nix
# Good
dontStrip = true;
```
</avoid_these>
</anti_patterns>

<troubleshooting>
<hash_mismatch>
**Error: "hash mismatch in fixed-output derivation"**

The hash you provided doesn't match what Nix fetched.

Solution:
1. Nix error shows "got: sha256-XYZ..."
2. Copy that hash into your derivation
3. Rebuild

For `fetchBunDeps`, this is expected the first time—use the error output to get the correct hash.
</hash_mismatch>

<missing_executable>
**Error: Binary not found after build**

Check:
```bash
# List what was actually built
ls -R result/

# Check package.json "bin" field
cat /nix/store/*-source/package.json | jq .bin

# Check build output location
cat /nix/store/*-source/package.json | jq .scripts.build
```

The build might output to a different directory than expected.
</missing_executable>

<elf_interpreter_error>
**Error: "No such file or directory" when running binary (Linux)**

The binary needs ELF patching for native dependencies.

Solution:
```nix
nativeBuildInputs = [
  autoPatchelfHook
];

buildInputs = [
  stdenv.cc.cc.lib
];
```

For node_modules with native addons:
```nix
buildPhase = ''
  cp -R ${node_modules}/node_modules .
  chmod -R u+w node_modules
  autoPatchelf node_modules  # Patch .node files
'';
```
</elf_interpreter_error>

<bun_lock_mismatch>
**Error: "bun.lock mismatch"**

The lockfile in your source doesn't match the cached dependencies.

This happens when:
- Source version updated but dependency hash not updated
- Source repo has uncommitted lockfile changes

Solution:
1. Update source hash to match new version
2. Set dependency hash to `lib.fakeHash`
3. Build to get correct dependency hash
4. Update dependency hash
5. Rebuild
</bun_lock_mismatch>
</troubleshooting>

<validation>
<build_checklist>
Before considering the package done:

- [ ] `nix build .#package-name` succeeds
- [ ] `./result/bin/tool --version` works
- [ ] `./result/bin/tool --help` works
- [ ] `nix flake check` passes
- [ ] `meta.description` is clear and concise
- [ ] `meta.homepage` points to project site
- [ ] `meta.license` is correct
- [ ] `meta.sourceProvenance` matches what you packaged
- [ ] `meta.mainProgram` is set
- [ ] `meta.platforms` is appropriate for the tool
- [ ] All hashes are real (no `lib.fakeHash`)
- [ ] Shebangs use Nix store paths, not /usr/bin
- [ ] File is formatted with `nix fmt`
</build_checklist>

<testing_on_other_platforms>
If you only have Linux but package claims `platforms.all`:

Consider asking maintainers with macOS/ARM to test, or:
- Mark platforms conservatively based on what you can test
- Note in package that other platforms are untested
- Let CI or other contributors expand platform support
</testing_on_other_platforms>
</validation>

<success_criteria>
A well-packaged npm tool has:

- Clean build with no warnings or errors
- Working executable in `result/bin/`
- Complete and accurate metadata
- Proper source provenance classification
- All dependencies resolved (no missing libraries)
- Reproducible builds (real hashes, no network access during build)
- Follows Nix packaging conventions (shebang patching, proper phases)
</success_criteria>
