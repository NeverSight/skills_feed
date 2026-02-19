---
name: cli-configuration
description: Configuration management patterns including file formats, precedence, environment variables, and XDG directories. Use when implementing configuration systems for CLI applications.
---

# CLI Configuration Skill

Patterns and best practices for managing configuration in command-line applications.

## Configuration Precedence

The standard precedence order (lowest to highest priority):

1. **Compiled defaults** - Hard-coded sensible defaults
2. **System config** - /etc/myapp/config.toml
3. **User config** - ~/.config/myapp/config.toml
4. **Project config** - ./myapp.toml or ./.myapp.toml
5. **Environment variables** - MYAPP_KEY=value
6. **CLI arguments** - --key value (highest priority)

```rust
use config::{Config as ConfigBuilder, Environment, File};

pub fn load_config(cli: &Cli) -> Result<Config> {
    let mut builder = ConfigBuilder::builder()
        // 1. Defaults
        .set_default("port", 8080)?
        .set_default("host", "localhost")?
        .set_default("log_level", "info")?;

    // 2. System config (if exists)
    builder = builder
        .add_source(File::with_name("/etc/myapp/config").required(false));

    // 3. User config (if exists)
    if let Some(config_dir) = dirs::config_dir() {
        builder = builder.add_source(
            File::from(config_dir.join("myapp/config.toml")).required(false)
        );
    }

    // 4. Project config (if exists)
    builder = builder
        .add_source(File::with_name("myapp").required(false))
        .add_source(File::with_name(".myapp").required(false));

    // 5. CLI-specified config (if provided)
    if let Some(config_path) = &cli.config {
        builder = builder.add_source(File::from(config_path.as_ref()));
    }

    // 6. Environment variables
    builder = builder.add_source(
        Environment::with_prefix("MYAPP")
            .separator("_")
            .try_parsing(true)
    );

    // 7. CLI arguments (highest priority)
    if let Some(port) = cli.port {
        builder = builder.set_override("port", port)?;
    }

    Ok(builder.build()?.try_deserialize()?)
}
```

## Config File Formats

### TOML (Recommended)

Clear, human-readable, good error messages.

```toml
# config.toml
[general]
port = 8080
host = "localhost"
log_level = "info"

[database]
url = "postgresql://localhost/mydb"
pool_size = 10

[features]
caching = true
metrics = false

[[servers]]
name = "primary"
address = "192.168.1.1"

[[servers]]
name = "backup"
address = "192.168.1.2"
```

```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
struct Config {
    general: General,
    database: Database,
    features: Features,
    servers: Vec<Server>,
}

#[derive(Debug, Deserialize, Serialize)]
struct General {
    port: u16,
    host: String,
    log_level: String,
}
```

### YAML (Alternative)

More concise, supports comments, complex structures.

```yaml
# config.yaml
general:
  port: 8080
  host: localhost
  log_level: info

database:
  url: postgresql://localhost/mydb
  pool_size: 10

features:
  caching: true
  metrics: false

servers:
  - name: primary
    address: 192.168.1.1
  - name: backup
    address: 192.168.1.2
```

### JSON (Machine-Readable)

Good for programmatic generation, less human-friendly.

```json
{
  "general": {
    "port": 8080,
    "host": "localhost",
    "log_level": "info"
  },
  "database": {
    "url": "postgresql://localhost/mydb",
    "pool_size": 10
  }
}
```

## XDG Base Directory Support

Follow the XDG Base Directory specification for cross-platform compatibility.

```rust
use directories::ProjectDirs;

pub struct AppPaths {
    pub config_dir: PathBuf,
    pub data_dir: PathBuf,
    pub cache_dir: PathBuf,
    pub state_dir: PathBuf,
}

impl AppPaths {
    pub fn new(app_name: &str) -> Result<Self> {
        let proj_dirs = ProjectDirs::from("com", "example", app_name)
            .ok_or_else(|| anyhow!("Could not determine project directories"))?;

        Ok(Self {
            config_dir: proj_dirs.config_dir().to_path_buf(),
            data_dir: proj_dirs.data_dir().to_path_buf(),
            cache_dir: proj_dirs.cache_dir().to_path_buf(),
            state_dir: proj_dirs.state_dir()
                .unwrap_or_else(|| proj_dirs.data_dir())
                .to_path_buf(),
        })
    }

    pub fn config_file(&self) -> PathBuf {
        self.config_dir.join("config.toml")
    }

    pub fn ensure_dirs(&self) -> Result<()> {
        fs::create_dir_all(&self.config_dir)?;
        fs::create_dir_all(&self.data_dir)?;
        fs::create_dir_all(&self.cache_dir)?;
        fs::create_dir_all(&self.state_dir)?;
        Ok(())
    }
}
```

**Directory locations by platform:**

| Platform | Config | Data | Cache |
|----------|--------|------|-------|
| Linux | ~/.config/myapp | ~/.local/share/myapp | ~/.cache/myapp |
| macOS | ~/Library/Application Support/myapp | ~/Library/Application Support/myapp | ~/Library/Caches/myapp |
| Windows | %APPDATA%\example\myapp | %APPDATA%\example\myapp | %LOCALAPPDATA%\example\myapp |

## Environment Variable Patterns

### Naming Convention

Use `APPNAME_SECTION_KEY` format:

```bash
MYAPP_DATABASE_URL=postgresql://localhost/db
MYAPP_LOG_LEVEL=debug
MYAPP_FEATURES_CACHING=true
MYAPP_PORT=9000
```

### Integration with Clap

```rust
#[derive(Parser)]
struct Cli {
    /// Database URL (env: MYAPP_DATABASE_URL)
    #[arg(long, env = "MYAPP_DATABASE_URL")]
    database_url: Option<String>,

    /// Log level (env: MYAPP_LOG_LEVEL)
    #[arg(long, env = "MYAPP_LOG_LEVEL", default_value = "info")]
    log_level: String,

    /// Port (env: MYAPP_PORT)
    #[arg(long, env = "MYAPP_PORT", default_value = "8080")]
    port: u16,
}
```

### Sensitive Data Pattern

**Never** put secrets in config files. Use environment variables instead.

```rust
#[derive(Debug, Deserialize)]
struct Config {
    pub host: String,
    pub port: u16,

    // Loaded from environment only
    #[serde(skip)]
    pub api_token: String,
}

impl Config {
    pub fn load() -> Result<Self> {
        let mut config: Config = /* load from file */;

        // Sensitive data from env only
        config.api_token = env::var("MYAPP_API_TOKEN")
            .context("MYAPP_API_TOKEN environment variable required")?;

        Ok(config)
    }
}
```

## Configuration Validation

Validate configuration early at load time:

```rust
#[derive(Debug, Deserialize)]
struct Config {
    pub port: u16,
    pub host: String,
    pub workers: usize,
}

impl Config {
    pub fn validate(&self) -> Result<()> {
        // Port range
        if !(1024..=65535).contains(&self.port) {
            bail!("Port must be between 1024 and 65535, got {}", self.port);
        }

        // Workers
        if self.workers == 0 {
            bail!("Workers must be at least 1");
        }

        let max_workers = num_cpus::get() * 2;
        if self.workers > max_workers {
            bail!(
                "Workers ({}) exceeds recommended maximum ({})",
                self.workers,
                max_workers
            );
        }

        // Host validation
        if self.host.is_empty() {
            bail!("Host cannot be empty");
        }

        Ok(())
    }
}
```

## Generating Default Config

Provide a command to generate a default configuration file:

```rust
impl Config {
    pub fn default_config() -> Self {
        Self {
            general: General {
                port: 8080,
                host: "localhost".to_string(),
                log_level: "info".to_string(),
            },
            database: Database {
                url: "postgresql://localhost/mydb".to_string(),
                pool_size: 10,
            },
            features: Features {
                caching: true,
                metrics: false,
            },
        }
    }

    pub fn write_default(path: &Path) -> Result<()> {
        let config = Self::default_config();
        let toml = toml::to_string_pretty(&config)?;

        // Add helpful comments
        let content = format!(
            "# Configuration file for myapp\n\
             # See: https://example.com/docs/config\n\n\
             {toml}"
        );

        fs::write(path, content)?;
        Ok(())
    }
}
```

**CLI Command:**

```rust
#[derive(Subcommand)]
enum Commands {
    /// Generate a default configuration file
    InitConfig {
        /// Output path (default: ~/.config/myapp/config.toml)
        #[arg(short, long)]
        output: Option<PathBuf>,
    },
}

fn handle_init_config(output: Option<PathBuf>) -> Result<()> {
    let path = output.unwrap_or_else(|| {
        AppPaths::new("myapp")
            .unwrap()
            .config_file()
    });

    if path.exists() {
        bail!("Config file already exists: {}", path.display());
    }

    Config::write_default(&path)?;
    println!("Created config file: {}", path.display());
    Ok(())
}
```

## Config Migration Pattern

Handle breaking changes in config format:

```rust
#[derive(Debug, Deserialize)]
struct ConfigV2 {
    version: u32,
    #[serde(flatten)]
    data: ConfigData,
}

impl ConfigV2 {
    pub fn load(path: &Path) -> Result<Self> {
        let content = fs::read_to_string(path)?;
        let mut config: ConfigV2 = toml::from_str(&content)?;

        // Migrate from older versions
        match config.version {
            1 => {
                eprintln!("Migrating config from v1 to v2...");
                config = migrate_v1_to_v2(config)?;
                // Optionally save migrated config
                config.save(path)?;
            }
            2 => {}, // Current version
            v => bail!("Unsupported config version: {}", v),
        }

        Ok(config)
    }
}
```

## Configuration Examples Command

Provide examples in help text:

```rust
#[derive(Subcommand)]
enum Commands {
    /// Show configuration examples
    ConfigExamples,
}

fn show_config_examples() {
    println!("Configuration Examples:\n");

    println!("1. Basic configuration (config.toml):");
    println!("{}", r#"
[general]
port = 8080
host = "localhost"
"#);

    println!("\n2. Environment variables:");
    println!("   MYAPP_PORT=9000");
    println!("   MYAPP_DATABASE_URL=postgresql://localhost/db");

    println!("\n3. CLI override:");
    println!("   myapp --port 9000 --host 0.0.0.0");

    println!("\n4. Precedence (highest to lowest):");
    println!("   CLI args > Env vars > Config file > Defaults");
}
```

## Best Practices

1. **Provide sensible defaults** - App should work out-of-box
2. **Document precedence** - Make override behavior clear
3. **Validate early** - Catch config errors at startup
4. **Use XDG directories** - Follow platform conventions
5. **Support env vars** - Essential for containers/CI
6. **Generate defaults** - Help users get started
7. **Version config format** - Enable migrations
8. **Keep secrets out** - Use env vars for sensitive data
9. **Clear error messages** - Help users fix config issues
10. **Document all options** - With examples and defaults

## References

- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [The Twelve-Factor App: Config](https://12factor.net/config)
- [directories crate](https://docs.rs/directories/)
- [config crate](https://docs.rs/config/)
