---
name: frankenphp
description: FrankenPHP Documentation - Modern PHP application server built on Caddy
---

# FrankenPHP Skill

Comprehensive assistance with FrankenPHP development - a modern PHP application server built on top of the Caddy web server. FrankenPHP enables persistent PHP processes with worker mode, automatic HTTPS, HTTP/2, HTTP/3, and real-time capabilities via Mercure integration.

## When to Use This Skill

This skill should be triggered when:
- Setting up or configuring FrankenPHP server
- Implementing FrankenPHP worker mode for performance optimization
- Integrating FrankenPHP with Laravel, Symfony, or other PHP frameworks
- Deploying PHP applications with Docker using FrankenPHP
- Converting traditional PHP apps to use persistent workers
- Configuring automatic HTTPS, HTTP/2, or HTTP/3
- Implementing real-time features with Mercure
- Creating standalone, self-executable PHP applications
- Optimizing PHP application performance with persistent processes
- Troubleshooting FrankenPHP worker mode or configuration issues

## Quick Reference

### Installation & Basic Server

**Install via curl (Linux/macOS):**
```bash
curl https://frankenphp.dev/install.sh | sh
mv frankenphp /usr/local/bin/

# Start server in current directory
frankenphp php-server
```

**Install via Homebrew:**
```bash
brew install dunglas/frankenphp/frankenphp
frankenphp php-server
```

**Quick Docker deployment:**
```bash
docker run -v $PWD:/app/public \
    -p 80:80 -p 443:443 -p 443:443/udp \
    dunglas/frankenphp
```

### Basic Worker Mode

**Start worker with standalone binary:**
```bash
frankenphp php-server --worker /path/to/your/worker/script.php
```

**Docker with worker mode:**
```bash
docker run \
    -e FRANKENPHP_CONFIG="worker /app/public/index.php" \
    -v $PWD:/app \
    -p 80:80 -p 443:443 -p 443:443/udp \
    dunglas/frankenphp
```

**Worker with 42 processes:**
```bash
docker run \
    -e FRANKENPHP_CONFIG="worker ./public/index.php 42" \
    -v $PWD:/app \
    -p 80:80 -p 443:443 -p 443:443/udp \
    dunglas/frankenphp
```

### Custom Worker Script

**Basic worker pattern:**
```php
<?php
// public/index.php

ignore_user_abort(true);

require __DIR__.'/vendor/autoload.php';

$myApp = new \App\Kernel();
$myApp->boot();

$handler = static function () use ($myApp) {
    try {
        echo $myApp->handle($_GET, $_POST, $_COOKIE, $_FILES, $_SERVER);
    } catch (\Throwable $exception) {
        (new \MyCustomExceptionHandler)->handleException($exception);
    }
};

$maxRequests = (int)($_SERVER['MAX_REQUESTS'] ?? 0);
for ($nbRequests = 0; !$maxRequests || $nbRequests < $maxRequests; ++$nbRequests) {
    $keepRunning = \frankenphp_handle_request($handler);
    $myApp->terminate();
    gc_collect_cycles();
    if (!$keepRunning) break;
}

$myApp->shutdown();
```

### Laravel Integration

**Laravel Octane installation:**
```bash
composer require laravel/octane
php artisan octane:install --server=frankenphp
php artisan octane:frankenphp
```

**Laravel with Docker:**
```bash
docker run -p 80:80 -p 443:443 -p 443:443/udp \
    -v $PWD:/app \
    dunglas/frankenphp
```

**Laravel Caddyfile:**
```
{
	frankenphp
}

localhost {
	root public/
	encode zstd br gzip
	php_server {
		try_files {path} index.php
	}
}
```

**Octane with file watching:**
```bash
php artisan octane:frankenphp --watch
```

### Symfony Integration

**Symfony worker with runtime:**
```bash
composer require runtime/frankenphp-symfony

docker run \
    -e FRANKENPHP_CONFIG="worker ./public/index.php" \
    -e APP_RUNTIME=Runtime\\FrankenPhpSymfony\\Runtime \
    -v $PWD:/app \
    -p 80:80 -p 443:443 -p 443:443/udp \
    dunglas/frankenphp
```

### Worker Management

**Watch files for changes (auto-reload):**
```bash
frankenphp php-server --worker /path/to/worker.php \
    --watch="/path/to/your/app/**/*.php"
```

**Restart workers via API:**
```bash
curl -X POST http://localhost:2019/frankenphp/workers/restart
```

**Configure max consecutive failures (Caddyfile):**
```
frankenphp {
    worker {
        max_consecutive_failures 10
    }
}
```

### Superglobals in Worker Mode

**Accessing worker-bound vs request-bound values:**
```php
<?php
// Capture worker-level values before request loop
$workerServer = $_SERVER;

$handler = static function () use ($workerServer) {
    var_dump($_SERVER);      // Current request superglobals
    var_dump($workerServer); // Original worker values
};
```

## Key Concepts

### Worker Mode
FrankenPHP's worker mode keeps your PHP application loaded in memory between requests, dramatically improving performance. Instead of bootstrapping your application for each request (traditional PHP), the application boots once and handles thousands of requests with the same process.

**Benefits:**
- Boot your application once, handle requests in milliseconds
- Persistent database connections
- Preloaded classes and configuration
- Significantly reduced memory overhead

**Key Pattern:** Use `frankenphp_handle_request($handler)` to process each request within a persistent loop, calling `gc_collect_cycles()` after each request to prevent memory leaks.

### Caddy Integration
FrankenPHP is built on top of Caddy, meaning you get:
- **Automatic HTTPS** - Zero-config TLS certificates via Let's Encrypt
- **HTTP/2 & HTTP/3** - Modern protocol support out of the box
- **Powerful configuration** - Use Caddyfile for server configuration

### Early Hints (103 Status)
FrankenPHP supports HTTP 103 Early Hints, allowing browsers to start loading critical resources (CSS, JS, fonts) while the server is still generating the full response.

### Mercure Real-Time
Built-in support for Mercure protocol enables real-time push notifications from server to browser using Server-Sent Events (SSE). Perfect for live updates, notifications, and collaborative features.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Core FrankenPHP documentation including installation, configuration, worker mode, framework integration, deployment, and production setup

The reference file contains detailed information from the official FrankenPHP documentation at https://frankenphp.dev/docs/

Use the reference file when you need:
- Detailed installation instructions for different platforms
- Advanced Caddyfile configuration examples
- Framework-specific integration patterns (Laravel, Symfony, WordPress, etc.)
- Production deployment strategies
- Performance optimization techniques
- Static binary compilation guides
- Docker configuration options

## Working with This Skill

### For Beginners
1. **Start with basic installation** - Use the curl install script or Docker for quickest setup
2. **Run traditional PHP first** - Use `frankenphp php-server` without worker mode to verify setup
3. **Test with simple scripts** - Create a basic `index.php` to understand the server behavior
4. **Learn Caddyfile basics** - Understand how to configure domains and paths
5. **Gradually adopt worker mode** - Once comfortable, convert to worker mode for performance

### For Laravel Developers
1. **Use Laravel Octane** - The official integration provides the smoothest experience
2. **Start with Docker** - Use the official `dunglas/frankenphp` image
3. **Configure Mercure** - Add real-time capabilities to your Laravel app
4. **Optimize workers** - Tune worker count based on your traffic patterns
5. **Use file watching** - Enable `--watch` during development for auto-reload

### For Symfony Developers
1. **Install Symfony runtime** - Use `runtime/frankenphp-symfony` package
2. **Set APP_RUNTIME** - Configure environment variable for automatic integration
3. **Use worker mode** - Leverage persistent processes for maximum performance
4. **Deploy with Docker** - Use official containers for production

### For Production Deployment
1. **Review worker configuration** - Set appropriate worker count and max requests
2. **Configure failure handling** - Set `max_consecutive_failures` threshold
3. **Enable monitoring** - Use Caddy admin API for health checks and metrics
4. **Set up log analytics** - Configure structured JSON logs
5. **Plan restart strategy** - Use `MAX_REQUESTS` or manual API restarts to prevent memory leaks
6. **Test with load** - Validate performance under realistic traffic patterns

### For Docker Users
1. **Use official images** - Start with `dunglas/frankenphp` or `dunglas/frankenphp:static-builder`
2. **Mount your app** - Volume mount your code to `/app`
3. **Configure via ENV** - Use `FRANKENPHP_CONFIG` for worker setup
4. **Expose ports** - Map 80, 443 (TCP), and 443 (UDP) for HTTP/3
5. **Use localhost** - Access via `https://localhost` (not 127.0.0.1)

## Common Patterns

### Performance Optimization
- **Use worker mode** for all production applications
- **Set MAX_REQUESTS** to restart workers periodically (prevents memory leaks)
- **Call gc_collect_cycles()** after each request in custom workers
- **Tune worker count** based on CPU cores and memory available
- **Enable HTTP/2 push** for critical assets

### Development Workflow
- **Use --watch flag** for automatic reload during development
- **Traditional mode** for debugging (easier to trace issues)
- **Docker for consistency** across development and production environments
- **Caddyfile per environment** (dev, staging, prod) with different configs

### Error Handling
- **Wrap handlers** in try-catch blocks within worker loop
- **Log exceptions** but keep worker running
- **Use max_consecutive_failures** to restart problematic workers
- **Monitor worker health** via Caddy admin API

## Resources

### Official Documentation
- **Main docs:** https://frankenphp.dev/docs/
- **Worker mode guide:** https://frankenphp.dev/docs/worker/
- **Laravel integration:** https://frankenphp.dev/docs/laravel/
- **Symfony integration:** https://frankenphp.dev/docs/symfony/

### Framework Integration
- Laravel Octane: Official integration via `laravel/octane` package
- Symfony Runtime: Use `runtime/frankenphp-symfony` package
- WordPress, Drupal, Joomla, TYPO3: Supported frameworks
- API Platform: First-class FrankenPHP support

### Docker Images
- **Production:** `dunglas/frankenphp`
- **Static builder:** `dunglas/frankenphp:static-builder`
- **Latest tag:** Always includes PHP 8.4+ and popular extensions

## Notes

- FrankenPHP includes PHP 8.4 and most popular extensions in static binaries
- Can be embedded as a Go library via `net/http` for custom applications
- Worker mode requires careful superglobals management (use closures to capture state)
- HTTPS is automatic via Let's Encrypt (no certificate configuration needed)
- HTTP/3 support requires UDP port 443 to be accessible
- File watching uses system-specific file monitoring (efficient, no polling)

## Troubleshooting

### Worker Not Starting
- Check worker script path is absolute or relative to document root
- Verify worker script has no syntax errors (`php -l script.php`)
- Check file permissions (script must be readable)
- Review logs for initialization errors

### Memory Leaks in Workers
- Call `gc_collect_cycles()` after each request
- Set `MAX_REQUESTS` to restart workers periodically
- Avoid global state accumulation
- Check for unclosed resources (files, connections)

### Performance Issues
- Increase worker count (`FRANKENPHP_CONFIG="worker ./index.php 42"`)
- Check worker restart frequency (too frequent = performance loss)
- Review database connection pooling
- Monitor memory usage per worker
- Verify no blocking operations in request handler

### HTTPS Not Working
- Ensure ports 80 and 443 are accessible
- Check firewall rules
- Verify domain DNS points to server
- Use `localhost` (not 127.0.0.1) for local development
- Accept self-signed certificate in browser for local testing

## Updating

To stay current with FrankenPHP:
1. Follow the official GitHub repository for updates
2. Review changelog for breaking changes
3. Test updates in staging environment
4. Update Docker images regularly (`docker pull dunglas/frankenphp:latest`)
5. Check framework-specific integration docs for version compatibility
