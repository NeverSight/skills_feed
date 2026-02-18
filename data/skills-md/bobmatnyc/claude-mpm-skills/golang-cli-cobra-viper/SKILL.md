---
name: golang-cli-cobra-viper
description: "Building production-quality CLI tools with Cobra command framework and Viper configuration management"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Build robust CLI tools with Cobra's command framework and Viper's configuration management for production-grade developer tools"
    when_to_use: "Creating multi-command CLIs, building developer tools/utilities, implementing DevOps automation, requiring flexible configuration (flags + env vars + config files), adding shell completion"
    quick_start: "1. Define command structure with Cobra 2. Integrate Viper for config priority 3. Bind flags to Viper 4. Add shell completion 5. Test CLI commands"
  token_estimate:
    entry: 140
    full: 4500
context_limit: 700
tags:
  - cli
  - golang
  - cobra
  - viper
  - configuration
  - shell-completion
requires_tools: []
---

# Go CLI Development with Cobra & Viper

## Overview

Cobra and Viper are the industry-standard libraries for building production-quality CLIs in Go. Cobra provides command structure and argument parsing, while Viper manages configuration from multiple sources with clear precedence rules.

**Key Features:**
- 🎯 **Cobra Commands**: POSIX-compliant CLI with subcommands (`app verb noun --flag`)
- ⚙️ **Viper Config**: Unified configuration from flags, env vars, and config files
- 🔄 **Integration**: Seamless Cobra + Viper plumbing patterns
- 🐚 **Shell Completion**: Auto-generated completions for bash, zsh, fish, PowerShell
- ✅ **Production Ready**: Battle-tested by kubectl, docker, gh, hugo

**Used By**: Kubernetes (kubectl), Docker CLI, GitHub CLI (gh), Hugo, Helm, and 100+ major projects

## When to Use This Skill

Activate this skill when:
- Building multi-command CLI tools with subcommands
- Creating developer tools, project generators, or scaffolding utilities
- Implementing admin CLIs for services or infrastructure
- Requiring flexible configuration (flags > env vars > config files > defaults)
- Adding shell completion for frequently-used CLIs
- Building DevOps automation tools or deployment scripts

## Cobra Framework

### Command Structure Pattern

Cobra follows the `APPNAME VERB NOUN --FLAG` pattern popularized by git and kubectl.

```go
// cmd/root.go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var cfgFile string

var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "A powerful CLI tool for developers",
    Long: `MyApp is a CLI tool that demonstrates best practices
for building production-quality command-line applications.

Complete documentation is available at https://myapp.example.com`,
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}

func init() {
    cobra.OnInitialize(initConfig)

    // Persistent flags (available to all subcommands)
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is $HOME/.myapp.yaml)")
    rootCmd.PersistentFlags().Bool("verbose", false, "verbose output")

    // Bind persistent flags to viper
    viper.BindPFlag("config", rootCmd.PersistentFlags().Lookup("config"))
    viper.BindPFlag("verbose", rootCmd.PersistentFlags().Lookup("verbose"))
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        if err != nil {
            fmt.Fprintln(os.Stderr, err)
            os.Exit(1)
        }

        viper.AddConfigPath(home)
        viper.AddConfigPath(".")
        viper.SetConfigType("yaml")
        viper.SetConfigName(".myapp")
    }

    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()

    if err := viper.ReadInConfig(); err == nil {
        if viper.GetBool("verbose") {
            fmt.Println("Using config file:", viper.ConfigFileUsed())
        }
    }
}
```

### Subcommands with Arguments

```go
// cmd/deploy.go
package cmd

import (
    "fmt"

    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

var deployCmd = &cobra.Command{
    Use:   "deploy [environment]",
    Short: "Deploy application to specified environment",
    Long: `Deploy the application to the specified environment.
Supports: dev, staging, production`,
    Args: cobra.ExactArgs(1),
    ValidArgs: []string{"dev", "staging", "production"},
    PreRunE: func(cmd *cobra.Command, args []string) error {
        // Validation logic runs before RunE
        env := args[0]
        if env == "production" && !viper.GetBool("force") {
            return fmt.Errorf("production deploys require --force flag")
        }
        return nil
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        env := args[0]
        region := viper.GetString("region")
        force := viper.GetBool("force")

        fmt.Printf("Deploying to %s in region %s (force=%v)\n", env, region, force)

        // Actual deployment logic
        return deploy(env, region, force)
    },
    PostRunE: func(cmd *cobra.Command, args []string) error {
        // Cleanup or notifications
        fmt.Println("Deployment complete")
        return nil
    },
}

func init() {
    rootCmd.AddCommand(deployCmd)

    // Local flags (only for this command)
    deployCmd.Flags().StringP("region", "r", "us-east-1", "AWS region")
    deployCmd.Flags().BoolP("force", "f", false, "Force deployment without confirmation")

    // Bind flags to viper
    viper.BindPFlag("region", deployCmd.Flags().Lookup("region"))
    viper.BindPFlag("force", deployCmd.Flags().Lookup("force"))
}

func deploy(env, region string, force bool) error {
    // Implementation
    return nil
}
```

### Persistent vs. Local Flags

```go
// Persistent flags: Available to command and all subcommands
rootCmd.PersistentFlags().String("config", "", "config file path")
rootCmd.PersistentFlags().Bool("verbose", false, "verbose output")

// Local flags: Only available to this specific command
deployCmd.Flags().String("region", "us-east-1", "deployment region")
deployCmd.Flags().Bool("force", false, "force deployment")

// Required flags
deployCmd.MarkFlagRequired("region")

// Flag dependencies
deployCmd.MarkFlagsRequiredTogether("username", "password")
deployCmd.MarkFlagsMutuallyExclusive("json", "yaml")
```

### PreRun/PostRun Hooks

Cobra provides execution hooks for setup and cleanup:

```go
var serverCmd = &cobra.Command{
    Use:   "server",
    Short: "Start API server",

    // Execution order (all optional):
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Runs before PreRunE, inherited by subcommands
        return setupLogging()
    },
    PreRunE: func(cmd *cobra.Command, args []string) error {
        // Validation and setup before RunE
        return validateConfig()
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        // Main command logic
        return startServer()
    },
    PostRunE: func(cmd *cobra.Command, args []string) error {
        // Cleanup after RunE
        return cleanup()
    },
    PersistentPostRunE: func(cmd *cobra.Command, args []string) error {
        // Runs after PostRunE, inherited by subcommands
        return flushLogs()
    },
}
```

**Important**: Use `RunE`, `PreRunE`, `PostRunE` (error-returning versions) instead of `Run`, `PreRun`, `PostRun`.

## Viper Configuration Management

### Configuration Priority

Viper follows a strict precedence order (highest to lowest):

1. **Explicit Set** (`viper.Set("key", value)`)
2. **Command-line Flags** (bound with `viper.BindPFlag`)
3. **Environment Variables** (`MYAPP_KEY=value`)
4. **Config File** (`~/.myapp.yaml`, `./config.yaml`)
5. **Key/Value Store** (etcd, Consul - optional)
6. **Defaults** (`viper.SetDefault("key", value)`)

```go
func initConfig() {
    // 1. Set defaults (lowest priority)
    viper.SetDefault("port", 8080)
    viper.SetDefault("database.host", "localhost")
    viper.SetDefault("database.port", 5432)

    // 2. Config file locations (checked in order)
    viper.SetConfigName("config")
    viper.SetConfigType("yaml")
    viper.AddConfigPath("/etc/myapp/")
    viper.AddConfigPath("$HOME/.myapp")
    viper.AddConfigPath(".")

    // 3. Environment variables (prefix + automatic mapping)
    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv() // MYAPP_PORT, MYAPP_DATABASE_HOST, etc.

    // 4. Read config file (optional)
    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); ok {
            // Config file not found - use defaults and env vars
        } else {
            // Config file found but error reading it
            return err
        }
    }

    // 5. Flags will be bound in init() functions (highest priority)
}
```

### Environment Variable Mapping

Viper automatically maps environment variables with prefix and dot notation:

```go
viper.SetEnvPrefix("MYAPP") // Prefix for env vars
viper.AutomaticEnv()        // Enable automatic mapping

// Config key → Environment variable
// "port"              → MYAPP_PORT
// "database.host"     → MYAPP_DATABASE_HOST
// "database.port"     → MYAPP_DATABASE_PORT
// "aws.s3.region"     → MYAPP_AWS_S3_REGION
```

**Manual mapping** for non-standard env var names:

```go
viper.BindEnv("database.host", "DB_HOST")          // Custom env var name
viper.BindEnv("database.password", "DB_PASSWORD")  // Different naming convention
```

### Config File Formats

Viper supports multiple formats: YAML, JSON, TOML, HCL, INI, envfile, Java properties.

**config.yaml**:
```yaml
port: 8080
log_level: info

database:
  host: localhost
  port: 5432
  user: postgres
  ssl_mode: require

aws:
  region: us-east-1
  s3:
    bucket: my-app-bucket
```

**Accessing config values**:
```go
port := viper.GetInt("port")                    // 8080
dbHost := viper.GetString("database.host")      // "localhost"
s3Bucket := viper.GetString("aws.s3.bucket")    // "my-app-bucket"

// Type-safe access
if viper.IsSet("database.ssl_mode") {
    sslMode := viper.GetString("database.ssl_mode")
}

// Unmarshal into struct
type Config struct {
    Port     int    `mapstructure:"port"`
    LogLevel string `mapstructure:"log_level"`
    Database struct {
        Host    string `mapstructure:"host"`
        Port    int    `mapstructure:"port"`
        User    string `mapstructure:"user"`
        SSLMode string `mapstructure:"ssl_mode"`
    } `mapstructure:"database"`
}

var config Config
if err := viper.Unmarshal(&config); err != nil {
    return err
}
```

## Cobra + Viper Integration

### Critical Integration Pattern

The key to Cobra + Viper integration is binding flags to Viper keys:

```go
// cmd/root.go
func init() {
    cobra.OnInitialize(initConfig) // Load config before command execution

    // Define flags
    rootCmd.PersistentFlags().String("config", "", "config file")
    rootCmd.PersistentFlags().String("log-level", "info", "log level")
    rootCmd.PersistentFlags().Int("port", 8080, "server port")

    // Bind flags to Viper (critical step!)
    viper.BindPFlag("config", rootCmd.PersistentFlags().Lookup("config"))
    viper.BindPFlag("log_level", rootCmd.PersistentFlags().Lookup("log-level"))
    viper.BindPFlag("port", rootCmd.PersistentFlags().Lookup("port"))
}

func initConfig() {
    // This runs BEFORE command execution via cobra.OnInitialize
    if cfgFile := viper.GetString("config"); cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        viper.AddConfigPath("$HOME/.myapp")
        viper.AddConfigPath(".")
        viper.SetConfigName("config")
    }

    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()

    viper.ReadInConfig() // Ignore errors - config file is optional
}
```

**Flag binding strategies**:

```go
// Strategy 1: Bind each flag individually (explicit)
viper.BindPFlag("log_level", rootCmd.Flags().Lookup("log-level"))

// Strategy 2: Bind all flags automatically (convenient)
viper.BindPFlags(rootCmd.Flags())

// Strategy 3: Hybrid approach (recommended)
// - Bind persistent flags globally
// - Bind local flags in each command's init()
rootCmd.PersistentFlags().String("config", "", "config file")
viper.BindPFlags(rootCmd.PersistentFlags())

deployCmd.Flags().String("region", "us-east-1", "AWS region")
viper.BindPFlag("deploy.region", deployCmd.Flags().Lookup("region"))
```

### PersistentPreRun for Config Loading

Use `PersistentPreRunE` to load and validate configuration:

```go
var rootCmd = &cobra.Command{
    Use:   "myapp",
    Short: "My application",
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        // Runs before ALL commands (inherited by subcommands)

        // 1. Validate required config
        if !viper.IsSet("api_key") {
            return fmt.Errorf("API key not configured (set MYAPP_API_KEY or add to config file)")
        }

        // 2. Setup logging based on config
        logLevel := viper.GetString("log_level")
        if err := setupLogging(logLevel); err != nil {
            return fmt.Errorf("invalid log level: %w", err)
        }

        // 3. Initialize clients/services
        apiKey := viper.GetString("api_key")
        if err := initAPIClient(apiKey); err != nil {
            return fmt.Errorf("failed to initialize API client: %w", err)
        }

        return nil
    },
}
```

## Shell Completion

Cobra generates shell completion scripts for bash, zsh, fish, and PowerShell.

### Adding Completion Command

```go
// cmd/completion.go
package cmd

import (
    "os"

    "github.com/spf13/cobra"
)

var completionCmd = &cobra.Command{
    Use:   "completion [bash|zsh|fish|powershell]",
    Short: "Generate shell completion script",
    Long: `Generate shell completion script for myapp.

To load completions:

Bash:
  $ source <(myapp completion bash)
  # To load automatically, add to ~/.bashrc:
  $ echo 'source <(myapp completion bash)' >> ~/.bashrc

Zsh:
  $ source <(myapp completion zsh)
  # To load automatically, add to ~/.zshrc:
  $ echo 'source <(myapp completion zsh)' >> ~/.zshrc

Fish:
  $ myapp completion fish | source
  # To load automatically:
  $ myapp completion fish > ~/.config/fish/completions/myapp.fish

PowerShell:
  PS> myapp completion powershell | Out-String | Invoke-Expression
  # To load automatically, add to PowerShell profile.
`,
    DisableFlagsInUseLine: true,
    ValidArgs:             []string{"bash", "zsh", "fish", "powershell"},
    Args:                  cobra.ExactValidArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        switch args[0] {
        case "bash":
            return cmd.Root().GenBashCompletion(os.Stdout)
        case "zsh":
            return cmd.Root().GenZshCompletion(os.Stdout)
        case "fish":
            return cmd.Root().GenFishCompletion(os.Stdout, true)
        case "powershell":
            return cmd.Root().GenPowerShellCompletionWithDesc(os.Stdout)
        }
        return nil
    },
}

func init() {
    rootCmd.AddCommand(completionCmd)
}
```

### Custom Completion Functions

Provide dynamic completions for command arguments:

```go
var deployCmd = &cobra.Command{
    Use:   "deploy [environment]",
    Short: "Deploy to environment",
    Args:  cobra.ExactArgs(1),
    ValidArgsFunction: func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        // Return available environments
        envs := []string{"dev", "staging", "production"}
        return envs, cobra.ShellCompDirectiveNoFileComp
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        return deploy(args[0])
    },
}

// Custom flag completion
deployCmd.RegisterFlagCompletionFunc("region", func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
    regions := []string{"us-east-1", "us-west-2", "eu-west-1"}
    return regions, cobra.ShellCompDirectiveNoFileComp
})
```

## CLI Best Practices

### User-Friendly Error Messages

```go
// ❌ BAD: Technical jargon
return fmt.Errorf("db connection failed: EOF")

// ✅ GOOD: Actionable error message
return fmt.Errorf("cannot connect to database at %s:%d\nPlease check:\n  - Database is running\n  - Credentials are correct (MYAPP_DB_PASSWORD)\n  - Network connectivity", host, port)

// ✅ GOOD: Suggest remediation
if !viper.IsSet("api_key") {
    return fmt.Errorf("API key not configured\nSet environment variable: export MYAPP_API_KEY=your-key\nOr add to config file: ~/.myapp.yaml")
}
```

### Progress Indicators

```go
import "github.com/briandowns/spinner"

func deploy(env string) error {
    s := spinner.New(spinner.CharSets[11], 100*time.Millisecond)
    s.Suffix = " Deploying to " + env + "..."
    s.Start()
    defer s.Stop()

    // Deployment logic
    if err := performDeployment(env); err != nil {
        s.Stop()
        return err
    }

    s.Stop()
    fmt.Println("✓ Deployment successful")
    return nil
}
```

### Output Formatting

```go
import (
    "encoding/json"
    "github.com/olekukonko/tablewriter"
)

func displayResults(items []Item, format string) error {
    switch format {
    case "json":
        enc := json.NewEncoder(os.Stdout)
        enc.SetIndent("", "  ")
        return enc.Encode(items)

    case "table":
        table := tablewriter.NewWriter(os.Stdout)
        table.SetHeader([]string{"ID", "Name", "Status"})
        for _, item := range items {
            table.Append([]string{item.ID, item.Name, item.Status})
        }
        table.Render()
        return nil

    default:
        return fmt.Errorf("unknown format: %s (use json or table)", format)
    }
}
```

### Logging vs. User Output

```go
import (
    "log"
    "os"
)

var (
    // User-facing output (stdout)
    out = os.Stdout

    // Logging and errors (stderr)
    logger = log.New(os.Stderr, "[myapp] ", log.LstdFlags)
)

func RunCommand() error {
    // User output: stdout
    fmt.Fprintln(out, "Processing files...")

    // Debug/verbose logging: stderr
    if viper.GetBool("verbose") {
        logger.Println("Reading config from", viper.ConfigFileUsed())
    }

    // Errors: stderr
    if err := process(); err != nil {
        fmt.Fprintf(os.Stderr, "Error: %v\n", err)
        return err
    }

    // Success message: stdout
    fmt.Fprintln(out, "✓ Complete")
    return nil
}
```

## Testing CLI Applications

### Testing Command Execution

```go
// cmd/deploy_test.go
package cmd

import (
    "bytes"
    "testing"

    "github.com/spf13/cobra"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func executeCommand(root *cobra.Command, args ...string) (output string, err error) {
    buf := new(bytes.Buffer)
    root.SetOut(buf)
    root.SetErr(buf)
    root.SetArgs(args)

    err = root.Execute()
    return buf.String(), err
}

func TestDeployCommand(t *testing.T) {
    tests := []struct {
        name    string
        args    []string
        wantErr bool
        wantOut string
    }{
        {
            name:    "deploy to dev",
            args:    []string{"deploy", "dev"},
            wantErr: false,
            wantOut: "Deploying to dev",
        },
        {
            name:    "deploy to production without force",
            args:    []string{"deploy", "production"},
            wantErr: true,
            wantOut: "production deploys require --force flag",
        },
        {
            name:    "deploy to production with force",
            args:    []string{"deploy", "production", "--force"},
            wantErr: false,
            wantOut: "Deploying to production",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            output, err := executeCommand(rootCmd, tt.args...)

            if tt.wantErr {
                require.Error(t, err)
            } else {
                require.NoError(t, err)
            }

            assert.Contains(t, output, tt.wantOut)
        })
    }
}
```

### Testing with Viper Configuration

```go
func TestCommandWithConfig(t *testing.T) {
    // Reset viper state before each test
    viper.Reset()

    // Set test configuration
    viper.Set("region", "eu-west-1")
    viper.Set("api_key", "test-key-123")

    output, err := executeCommand(rootCmd, "deploy", "staging")

    require.NoError(t, err)
    assert.Contains(t, output, "eu-west-1")
}
```

### Capturing Output

```go
func TestOutputFormat(t *testing.T) {
    // Capture stdout
    oldStdout := os.Stdout
    r, w, _ := os.Pipe()
    os.Stdout = w
    defer func() { os.Stdout = oldStdout }()

    // Execute command
    err := listCmd.RunE(listCmd, []string{})
    require.NoError(t, err)

    // Read output
    w.Close()
    var buf bytes.Buffer
    io.Copy(&buf, r)
    output := buf.String()

    assert.Contains(t, output, "ID")
    assert.Contains(t, output, "Name")
}
```

## Decision Trees

### When to Use Cobra

**Use Cobra when:**
- ✅ Building multi-command CLI with subcommands (e.g., `git clone`, `docker run`)
- ✅ Need POSIX-compliant flag parsing (`--flag`, `-f`)
- ✅ Want built-in help generation (`--help`)
- ✅ Require shell completion support
- ✅ Building professional CLI used by other developers

**Don't use Cobra when:**
- ❌ Simple single-command script (use `flag` package)
- ❌ Internal-only tool with 1-2 flags
- ❌ Prototyping or throwaway scripts

### When to Use Viper

**Use Viper when:**
- ✅ Need configuration from multiple sources (flags, env vars, files)
- ✅ Want clear configuration precedence rules
- ✅ Support multiple config file formats (YAML, JSON, TOML)
- ✅ Require environment variable mapping with prefixes
- ✅ Need live config reloading (watch config file changes)

**Don't use Viper when:**
- ❌ Only using command-line flags (Cobra alone is sufficient)
- ❌ Hardcoded configuration values
- ❌ Simple scripts with no configuration

### When to Add Shell Completion

**Add shell completion when:**
- ✅ CLI used frequently by developers (daily/hourly)
- ✅ Many subcommands or complex flag combinations
- ✅ Arguments have known valid values (e.g., environments, regions)
- ✅ Building professional developer tools

**Skip shell completion when:**
- ❌ CLI used rarely (monthly or less)
- ❌ Simple commands with few options
- ❌ Internal-only tools

### When to Use Persistent Flags

**Use persistent flags when:**
- ✅ Flag applies to ALL subcommands (e.g., `--verbose`, `--config`)
- ✅ Common configuration shared across commands
- ✅ Global behavior modifiers (e.g., `--dry-run`, `--output`)

**Use local flags when:**
- ✅ Flag only relevant to specific command
- ✅ Command-specific parameters (e.g., `--region` for deploy command)

## Anti-Patterns

### ❌ Not Handling Errors in PreRunE/RunE

**Wrong**:
```go
var deployCmd = &cobra.Command{
    Use: "deploy",
    Run: func(cmd *cobra.Command, args []string) {
        deploy(args[0]) // Ignores error!
    },
}
```

**Correct**:
```go
var deployCmd = &cobra.Command{
    Use: "deploy",
    RunE: func(cmd *cobra.Command, args []string) error {
        return deploy(args[0]) // Proper error handling
    },
}
```

### ❌ Mixing Configuration Sources Without Clear Precedence

**Wrong**:
```go
// Confusing: Which takes precedence?
config.Port = viper.GetInt("port")
if os.Getenv("PORT") != "" {
    config.Port = atoi(os.Getenv("PORT"))
}
if *flagPort != 0 {
    config.Port = *flagPort
}
```

**Correct**:
```go
// Clear: Viper handles precedence automatically
viper.BindPFlag("port", rootCmd.Flags().Lookup("port"))
viper.SetEnvPrefix("MYAPP")
viper.AutomaticEnv()
viper.SetDefault("port", 8080)

config.Port = viper.GetInt("port") // Respects: flag > env > config > default
```

### ❌ Forgetting to Bind Flags to Viper

**Wrong**:
```go
rootCmd.Flags().String("region", "us-east-1", "AWS region")
// Flag not bound to Viper - won't respect precedence!

func deploy() {
    region := viper.GetString("region") // Always returns config file value
}
```

**Correct**:
```go
rootCmd.Flags().String("region", "us-east-1", "AWS region")
viper.BindPFlag("region", rootCmd.Flags().Lookup("region")) // Bind it!

func deploy() {
    region := viper.GetString("region") // Respects flag > env > config
}
```

### ❌ Not Testing CLI Commands

**Wrong**:
```go
// No tests for CLI commands - bugs slip through
```

**Correct**:
```go
func TestDeployCommand(t *testing.T) {
    output, err := executeCommand(rootCmd, "deploy", "staging", "--region", "eu-west-1")
    require.NoError(t, err)
    assert.Contains(t, output, "Deploying to staging")
    assert.Contains(t, output, "eu-west-1")
}
```

### ❌ Poor Error Messages

**Wrong**:
```go
return fmt.Errorf("connection failed") // Unhelpful
```

**Correct**:
```go
return fmt.Errorf("cannot connect to database at %s:%d\nCheck:\n  - Database is running\n  - Credentials (MYAPP_DB_PASSWORD)\n  - Firewall rules", host, port)
```

### ❌ Using Run Instead of RunE

**Wrong**:
```go
var rootCmd = &cobra.Command{
    Use: "myapp",
    Run: func(cmd *cobra.Command, args []string) {
        if err := execute(); err != nil {
            fmt.Println(err) // Error not propagated
        }
    },
}
```

**Correct**:
```go
var rootCmd = &cobra.Command{
    Use: "myapp",
    RunE: func(cmd *cobra.Command, args []string) error {
        return execute() // Cobra handles error display and exit code
    },
}
```

## Production Example

Minimal production-ready CLI structure:

```
myapp/
├── cmd/
│   ├── root.go          # Root command + config loading
│   ├── deploy.go        # Deploy subcommand
│   ├── status.go        # Status subcommand
│   └── completion.go    # Shell completion
├── main.go              # Entry point
├── config.yaml          # Example config file
└── go.mod
```

**main.go**:
```go
package main

import "myapp/cmd"

func main() {
    cmd.Execute()
}
```

**cmd/root.go**: See "Command Structure Pattern" section above

**Building and installing**:
```bash
# Development
go run main.go deploy staging --region us-west-2

# Production build
go build -o myapp

# Install globally
go install

# Enable shell completion
myapp completion bash > /etc/bash_completion.d/myapp
```

## Resources

**Official Documentation**:
- [Cobra User Guide](https://cobra.dev/) - Official framework documentation
- [Viper Documentation](https://github.com/spf13/viper) - Configuration management guide

**Learning Resources**:
- "Building CLI Apps in Go with Cobra & Viper" (November 2025) - Comprehensive tutorial
- "The Cobra & Viper Journey" - Learning path for CLI development
- [Cobra Generator](https://github.com/spf13/cobra-cli) - Scaffolding tool for new CLIs

**Production Examples**:
- [kubectl](https://github.com/kubernetes/kubectl) - Kubernetes CLI
- [docker](https://github.com/docker/cli) - Docker CLI
- [gh](https://github.com/cli/cli) - GitHub CLI
- [hugo](https://github.com/gohugoio/hugo) - Static site generator

**Related Skills**:
- `golang-testing-strategies` - Testing CLI commands comprehensively
- `golang-http-servers` - Building API servers with configuration
- `golang-concurrency-patterns` - Async operations in CLI tools

## Success Criteria

You know you've mastered Cobra + Viper when:
- ✅ Commands follow POSIX conventions (`VERB NOUN --FLAG`)
- ✅ Configuration precedence is clear: flags > env > config > defaults
- ✅ All flags bound to Viper for unified config access
- ✅ Shell completion generated for all major shells
- ✅ Error messages are actionable and user-friendly
- ✅ CLI commands have comprehensive tests
- ✅ Help text auto-generated and accurate
- ✅ PersistentPreRunE used for global setup/validation
- ✅ Separation of concerns: user output (stdout) vs. logging (stderr)
- ✅ Config files optional - CLI works with flags/env vars alone
