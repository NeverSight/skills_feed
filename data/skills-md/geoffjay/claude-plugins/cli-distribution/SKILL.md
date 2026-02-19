---
name: cli-distribution
description: Distribution and packaging patterns including shell completions, man pages, cross-compilation, and release automation. Use when preparing CLI tools for distribution.
---

# CLI Distribution Skill

Patterns and best practices for distributing Rust CLI applications to users.

## Shell Completion Generation

### Using clap_complete

```rust
use clap::{CommandFactory, Parser};
use clap_complete::{generate, Generator, Shell};
use std::io;

#[derive(Parser)]
struct Cli {
    /// Generate shell completions
    #[arg(long = "generate", value_enum)]
    generator: Option<Shell>,

    // ... other fields
}

fn print_completions<G: Generator>(gen: G, cmd: &mut clap::Command) {
    generate(gen, cmd, cmd.get_name().to_string(), &mut io::stdout());
}

fn main() {
    let cli = Cli::parse();

    if let Some(generator) = cli.generator {
        let mut cmd = Cli::command();
        print_completions(generator, &mut cmd);
        return;
    }

    // ... rest of application
}
```

### Installation Instructions by Shell

**Bash:**
```bash
# Generate and save
myapp --generate bash > /etc/bash_completion.d/myapp

# Or add to ~/.bashrc
eval "$(myapp --generate bash)"
```

**Zsh:**
```bash
# Generate and save
myapp --generate zsh > ~/.zfunc/_myapp

# Add to ~/.zshrc
fpath=(~/.zfunc $fpath)
autoload -Uz compinit && compinit
```

**Fish:**
```bash
# Generate and save
myapp --generate fish > ~/.config/fish/completions/myapp.fish

# Or load directly
myapp --generate fish | source
```

**PowerShell:**
```powershell
# Add to $PROFILE
Invoke-Expression (& myapp --generate powershell)
```

### Dynamic Completions

For commands with dynamic values (like listing resources):

```rust
use clap::CommandFactory;
use clap_complete::{generate, Generator};

pub fn generate_with_values<G: Generator>(
    gen: G,
    resources: &[String],
) -> String {
    let mut cmd = Cli::command();

    // Add dynamic values to completion
    if let Some(subcommand) = cmd.find_subcommand_mut("get") {
        for resource in resources {
            subcommand = subcommand.arg(
                clap::Arg::new("resource")
                    .value_parser(clap::builder::PossibleValuesParser::new(resource))
            );
        }
    }

    let mut buf = Vec::new();
    generate(gen, &mut cmd, "myapp", &mut buf);
    String::from_utf8(buf).unwrap()
}
```

## Man Page Generation

### Using clap_mangen

```toml
[dependencies]
clap_mangen = "0.2"
```

```rust
use clap::CommandFactory;
use clap_mangen::Man;
use std::io;

fn generate_man_page() {
    let cmd = Cli::command();
    let man = Man::new(cmd);
    man.render(&mut io::stdout()).unwrap();
}
```

### Build Script for Man Pages

```rust
// build.rs
use clap::CommandFactory;
use clap_mangen::Man;
use std::fs;
use std::path::PathBuf;

include!("src/cli.rs");

fn main() {
    let out_dir = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("target/man");
    fs::create_dir_all(&out_dir).unwrap();

    let cmd = Cli::command();
    let man = Man::new(cmd);
    let mut buffer = Vec::new();
    man.render(&mut buffer).unwrap();

    fs::write(out_dir.join("myapp.1"), buffer).unwrap();
}
```

### Install Man Page

```bash
# System-wide
sudo cp target/man/myapp.1 /usr/local/share/man/man1/

# User-local
mkdir -p ~/.local/share/man/man1
cp target/man/myapp.1 ~/.local/share/man/man1/
```

## Cross-Compilation

### Target Triples

Common targets for CLI distribution:

```bash
# Linux
x86_64-unknown-linux-gnu      # GNU Linux
x86_64-unknown-linux-musl     # MUSL Linux (static)
aarch64-unknown-linux-gnu     # ARM64 Linux

# macOS
x86_64-apple-darwin           # Intel Mac
aarch64-apple-darwin          # Apple Silicon

# Windows
x86_64-pc-windows-msvc        # Windows MSVC
x86_64-pc-windows-gnu         # Windows GNU
```

### Cross-Compilation with cross

```bash
# Install cross
cargo install cross

# Build for Linux from any platform
cross build --release --target x86_64-unknown-linux-gnu

# Build static binary with MUSL
cross build --release --target x86_64-unknown-linux-musl
```

### GitHub Actions for Cross-Compilation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    strategy:
      matrix:
        include:
          - os: ubuntu-latest
            target: x86_64-unknown-linux-gnu
            artifact_name: myapp
            asset_name: myapp-linux-amd64

          - os: ubuntu-latest
            target: x86_64-unknown-linux-musl
            artifact_name: myapp
            asset_name: myapp-linux-musl-amd64

          - os: macos-latest
            target: x86_64-apple-darwin
            artifact_name: myapp
            asset_name: myapp-macos-amd64

          - os: macos-latest
            target: aarch64-apple-darwin
            artifact_name: myapp
            asset_name: myapp-macos-arm64

          - os: windows-latest
            target: x86_64-pc-windows-msvc
            artifact_name: myapp.exe
            asset_name: myapp-windows-amd64.exe

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v3

      - uses: dtolnay/rust-toolchain@stable
        with:
          targets: ${{ matrix.target }}

      - name: Build
        run: cargo build --release --target ${{ matrix.target }}

      - name: Upload binaries
        uses: actions/upload-artifact@v3
        with:
          name: ${{ matrix.asset_name }}
          path: target/${{ matrix.target }}/release/${{ matrix.artifact_name }}
```

## Binary Size Optimization

### Cargo.toml optimizations

```toml
[profile.release]
opt-level = "z"     # Optimize for size
lto = true          # Link-time optimization
codegen-units = 1   # Better optimization
strip = true        # Strip symbols
panic = "abort"     # Smaller panic handler
```

### Additional size reduction

```bash
# Install upx
brew install upx  # macOS
apt install upx   # Linux

# Compress binary
upx --best --lzma target/release/myapp
```

**Before/After example:**
```
Original:  2.5 MB
Optimized: 1.2 MB (strip = true)
UPX:       400 KB (upx --best --lzma)
```

## Package Distribution

### Homebrew (macOS/Linux)

Create a formula:

```ruby
# Formula/myapp.rb
class Myapp < Formula
  desc "Description of your CLI tool"
  homepage "https://github.com/username/myapp"
  url "https://github.com/username/myapp/archive/v1.0.0.tar.gz"
  sha256 "abc123..."
  license "MIT"

  depends_on "rust" => :build

  def install
    system "cargo", "install", "--locked", "--root", prefix, "--path", "."

    # Install shell completions
    generate_completions_from_executable(bin/"myapp", "--generate")

    # Install man page
    man1.install "target/man/myapp.1"
  end

  test do
    assert_match "myapp 1.0.0", shell_output("#{bin}/myapp --version")
  end
end
```

### Debian Package (.deb)

Using `cargo-deb`:

```bash
cargo install cargo-deb

# Create debian package
cargo deb

# Package will be in target/debian/myapp_1.0.0_amd64.deb
```

**Cargo.toml metadata:**

```toml
[package.metadata.deb]
maintainer = "Your Name <you@example.com>"
copyright = "2024, Your Name"
license-file = ["LICENSE", "4"]
extended-description = """
A longer description of your CLI tool
that spans multiple lines."""
depends = "$auto"
section = "utility"
priority = "optional"
assets = [
    ["target/release/myapp", "usr/bin/", "755"],
    ["README.md", "usr/share/doc/myapp/", "644"],
    ["target/completions/myapp.bash", "usr/share/bash-completion/completions/", "644"],
    ["target/man/myapp.1", "usr/share/man/man1/", "644"],
]
```

### Docker Distribution

```dockerfile
# Dockerfile
FROM rust:1.75 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/myapp /usr/local/bin/myapp
ENTRYPOINT ["myapp"]
```

**Multi-stage with MUSL (smaller image):**

```dockerfile
FROM rust:1.75-alpine as builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/myapp /myapp
ENTRYPOINT ["/myapp"]
```

### Cargo-binstall Support

Add metadata for faster installation:

```toml
[package.metadata.binstall]
pkg-url = "{ repo }/releases/download/v{ version }/{ name }-{ target }{ binary-ext }"
bin-dir = "{ bin }{ binary-ext }"
pkg-fmt = "bin"
```

Users can then install with:
```bash
cargo binstall myapp
```

## Auto-Update

### Using self_update crate

```toml
[dependencies]
self_update = "0.39"
```

```rust
use self_update::cargo_crate_version;

fn update() -> Result<()> {
    let status = self_update::backends::github::Update::configure()
        .repo_owner("username")
        .repo_name("myapp")
        .bin_name("myapp")
        .show_download_progress(true)
        .current_version(cargo_crate_version!())
        .build()?
        .update()?;

    println!("Update status: `{}`!", status.version());
    Ok(())
}
```

### Update Command

```rust
#[derive(Subcommand)]
enum Commands {
    /// Update to the latest version
    Update,
}

fn handle_update() -> Result<()> {
    println!("Checking for updates...");

    match update() {
        Ok(_) => {
            println!("Updated successfully! Please restart the application.");
            Ok(())
        }
        Err(e) => {
            eprintln!("Update failed: {}", e);
            eprintln!("Download manually: https://github.com/username/myapp/releases");
            Err(e)
        }
    }
}
```

## Release Automation

### Cargo-release

```bash
cargo install cargo-release

# Dry run
cargo release --dry-run

# Release patch version
cargo release patch --execute

# Release minor version
cargo release minor --execute
```

### GitHub Release Action

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: taiki-e/create-gh-release-action@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          changelog: CHANGELOG.md

  upload-assets:
    needs: release
    strategy:
      matrix:
        include:
          - target: x86_64-unknown-linux-gnu
          - target: x86_64-apple-darwin
          - target: x86_64-pc-windows-msvc

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3

      - uses: taiki-e/upload-rust-binary-action@v1
        with:
          bin: myapp
          target: ${{ matrix.target }}
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Best Practices

1. **Provide multiple installation methods** - Cargo, Homebrew, apt, etc.
2. **Generate completions** - Essential for good UX
3. **Create man pages** - Professional documentation
4. **Test cross-platform** - Build for all major platforms
5. **Optimize binary size** - Users appreciate smaller downloads
6. **Automate releases** - Use CI/CD for consistent builds
7. **Version clearly** - Semantic versioning
8. **Sign binaries** - Build trust (especially on macOS)
9. **Provide checksums** - Verify download integrity
10. **Document installation** - Clear, platform-specific instructions

## Distribution Checklist

- [ ] Shell completions generated (bash, zsh, fish, powershell)
- [ ] Man pages created
- [ ] Cross-compiled for major platforms
- [ ] Binary size optimized
- [ ] Release artifacts uploaded to GitHub
- [ ] Installation instructions in README
- [ ] Homebrew formula (if applicable)
- [ ] Debian package (if applicable)
- [ ] Docker image (if applicable)
- [ ] Checksums provided
- [ ] Changelog maintained
- [ ] Version bumped properly

## References

- [clap_complete Documentation](https://docs.rs/clap_complete/)
- [clap_mangen Documentation](https://docs.rs/clap_mangen/)
- [cargo-deb](https://github.com/kornelski/cargo-deb)
- [cross](https://github.com/cross-rs/cross)
- [Rust Platform Support](https://doc.rust-lang.org/nightly/rustc/platform-support.html)
