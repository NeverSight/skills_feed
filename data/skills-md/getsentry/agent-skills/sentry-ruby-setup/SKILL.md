---
name: sentry-ruby-setup
description: Setup Sentry in Ruby apps. Use when asked to add Sentry to Ruby, install sentry-ruby gem, or configure error monitoring for Ruby applications or Rails.
---

# Sentry Ruby Setup

Install and configure Sentry in Ruby projects.

## Invoke This Skill When

- User asks to "add Sentry to Ruby" or "install Sentry" in a Ruby app
- User wants error monitoring, logging, or tracing in Ruby
- User mentions "sentry-ruby" gem or Ruby on Rails

## Requirements

- Ruby 2.4+ or recent JRuby versions

## Install

Add to `Gemfile`:

```ruby
gem "sentry-ruby"

# For profiling, also add:
gem "stackprof"
```

Then run:

```bash
bundle install
```

## Configure

Initialize as early as possible:

```ruby
require "sentry-ruby"

Sentry.init do |config|
  config.dsn = "YOUR_SENTRY_DSN"
  config.send_default_pii = true
  
  # Breadcrumbs from logs
  config.breadcrumbs_logger = [:sentry_logger, :http_logger]
  
  # Tracing
  config.traces_sample_rate = 1.0
  
  # Profiling (requires stackprof gem)
  config.profiles_sample_rate = 1.0
  
  # Logs
  config.enable_logs = true
end
```

## Rails Integration

For Rails, add to `config/initializers/sentry.rb`:

```ruby
Sentry.init do |config|
  config.dsn = ENV["SENTRY_DSN"]
  config.send_default_pii = true
  config.breadcrumbs_logger = [:active_support_logger, :http_logger]
  config.traces_sample_rate = 1.0
  config.profiles_sample_rate = 1.0
  config.enable_logs = true
end
```

### Rails-specific Gems

```ruby
# Gemfile
gem "sentry-ruby"
gem "sentry-rails"  # Rails integration
gem "sentry-sidekiq"  # If using Sidekiq
gem "sentry-delayed_job"  # If using Delayed Job
gem "sentry-resque"  # If using Resque
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `dsn` | Sentry DSN | Required |
| `send_default_pii` | Include user data | `false` |
| `traces_sample_rate` | % of transactions traced | `0` |
| `profiles_sample_rate` | % of traces profiled | `0` |
| `enable_logs` | Send logs to Sentry | `false` |
| `environment` | Environment name | Auto-detected |
| `release` | Release version | Auto-detected |

## Breadcrumb Loggers

| Logger | Description |
|--------|-------------|
| `:sentry_logger` | Sentry's own logger |
| `:http_logger` | HTTP request breadcrumbs |
| `:active_support_logger` | Rails ActiveSupport (Rails only) |

## Environment Variables

```bash
SENTRY_DSN=https://xxx@o123.ingest.sentry.io/456
SENTRY_AUTH_TOKEN=sntrys_xxx
SENTRY_ORG=my-org
SENTRY_PROJECT=my-project
```

## Verification

```ruby
# Capture test message
Sentry.capture_message("Test message from Ruby")

# Or trigger intentional error
1 / 0
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Errors not appearing | Ensure `Sentry.init` called early, check DSN |
| No traces | Set `traces_sample_rate` > 0 |
| No profiles | Add `stackprof` gem, set `profiles_sample_rate` |
| Rails errors missing | Use `sentry-rails` gem instead of `sentry-ruby` |
