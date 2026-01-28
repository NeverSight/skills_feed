---
name: validate-aspire-runtime
description: Starts and validates the Aspire orchestrated application runtime. Use this skill to spin up the complete application environment (database, cache, API, Worker, UI) and verify that all resources reach healthy status before running E2E tests.
---

# Validate Aspire Runtime Skill

Use this skill to start the complete Aspire-orchestrated application and verify all services are running and healthy.

## What This Skill Does

1. Starts the Aspire runtime using `aspire run` command
2. Uses Aspire MCP `list_resources` tool to poll resource health
3. Waits for all critical resources to reach healthy status:
   - `sql-server` (database) - must be started
   - `cache` (Redis) - must be started
   - `api` (main API service) - must be healthy
   - `worker` (background worker) - must be started
   - `ui` (frontend app) - must be started
4. Extracts the UI endpoint URL from resources (typically `https://localhost:3000`)
5. Communicates the UI endpoint URL back to the agent for use in E2E validation
6. Exits with failure if startup fails or health checks don't pass

## When to Use

- After backend and frontend builds succeed
- After all tests pass
- To prepare the application for interactive E2E validation
- To verify the complete system works together before E2E testing

## How the Agent Should Use This Skill

1. **Prepare**: Ensure all previous validation steps (builds, tests) have succeeded
2. **Start Aspire**: Run Aspire in a terminal/background process:
   ```
   aspire run
   ```
   This will start the Aspire dashboard and orchestrate all resources.

3. **Check Resources**: Use the Aspire MCP `list_resources` tool to monitor resource status:
   - Call `list_resources` repeatedly until all resources reach healthy state
   - Monitor for errors or failed startup
   - Expected resource states: `Running` or `Healthy`

4. **Extract Endpoint**: Once `ui` resource is healthy, extract its HTTP endpoint (typically `https://localhost:3000`)

5. **Communicate Endpoint**: Report the discovered UI endpoint URL to use in the next E2E validation step

6. **Monitor Startup**: Typical startup sequence:
   - SQL Server starts (takes 5-10 seconds)
   - Redis starts (takes 2-3 seconds)
   - API service starts and runs health checks (takes 5-15 seconds)
   - Worker service starts (takes 3-5 seconds)
   - UI starts and connects to API (takes 5-10 seconds)

7. **Handle Failures**: If any resource fails to start or becomes unhealthy:
   - Check Aspire dashboard logs for error messages
   - Report the specific resource and error to user
   - Halt further validation

## Success Criteria

- Aspire process is running and accepting connections
- `list_resources` returns all resources with healthy status
- `ui` resource shows HTTP endpoint URL (typically `https://localhost:3000`)
- No error logs from resources

## Failure Indicators

- Aspire startup fails or crashes
- Resources remain in `Failed` or `Unhealthy` state after timeout
- Health check endpoints return non-2xx status
- Logs show connection/initialization errors

## Resource Details Reference

### Resource Startup Order (from AppHost.cs)
1. **sql-server** - Base resource, must start first
2. **cache** - Base resource, starts independently
3. **api** - Depends on sql-server + cache, includes Dapr sidecar
4. **worker** - Depends on sql-server + cache
5. **ui** - Depends on api, Vite app

### Health Check Endpoints (on API)
- `GET /health/live` - Liveness probe (is service running)
- `GET /health/ready` - Readiness probe (can service handle requests)

### Endpoint Mappings
- SQL Server: `localhost:1433`
- Redis: `localhost:6379`
- RedisInsight: `http://localhost:8001`
- API (internal): `http://localhost:17623`
- UI: `https://localhost:3000`
- Aspire Dashboard: `http://localhost:19888`

## Important Notes

- **First run**: First time running Aspire may take longer due to container pulls/initialization
- **Dapr**: API service includes Dapr sidecar; Dapr runtime is auto-managed by Aspire
- **Database**: Uses persistent data volume; survives restarts during development
- **Certificates**: UI uses developer certificates for HTTPS (auto-trusted on first run)
- **Logs**: Full resource logs available through Aspire dashboard or `list_structured_logs` tool

## Cleaning Up After Validation

After E2E validation completes (success or failure):
1. Stop Aspire by pressing `Ctrl+C` in the terminal running `aspire run`
2. Aspire will gracefully shut down all resources
3. For next validation run, start `aspire run` again

## Next Steps After Success

Once all resources are healthy and UI endpoint is confirmed:
- **Validate E2E Skill** - to run interactive UI navigation and feature validation
