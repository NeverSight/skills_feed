---
name: devops-pathfinders
description: Advanced DevOps skill for managing Debian 12 VPS servers on Contabo with Docker, Nginx, and MySQL infrastructure. Use when working with server setup, Docker deployments, SSL configuration, security hardening, backup strategies, troubleshooting access issues, container management, Nginx reverse proxy configuration, or any DevOps task on the Pathfinders Labs infrastructure. Specialized in KISS (Keep It Simple, Stupid) approach with single Docker network, shared MySQL, native Nginx, and centralized credentials management.
---

# DevOps Pathfinders - Advanced Server Management

Skill especializado para gestión avanzada de infraestructura Pathfinders Labs en Contabo con Debian 12.

## Philosophy: KISS (Keep It Simple, Stupid)

Esta skill implementa infraestructura simple, funcional y mantenible:

- **Una red Docker:** `pathfinders` - todos los contenedores la comparten
- **MySQL compartida:** Un contenedor MariaDB para todos los servicios
- **Nginx nativo:** Sin Docker, instalado directamente en el servidor
- **Credenciales centralizadas:** Un archivo `/opt/pathfinders/.credentials`
- **SSL wildcard:** Un certificado para todos los subdominios
- **Docker Compose simple:** Un archivo por servicio, sin orquestadores

## Infrastructure Overview

**Servidor:** 173.212.247.69 (Contabo VPS)  
**OS:** Debian 12 (Bookworm)  
**Disco:** 200GB  
**Estructura:** Todo en `/opt/pathfinders/`  
**Red Docker:** `pathfinders` (bridge externa)  
**Dominio:** internationalpathfinders.com (wildcard SSL)

## Quick Reference

### Read Infrastructure Documentation First

**ALWAYS start by reading the infrastructure documentation:**

```bash
view references/infrastructure.md
```

This contains critical information about server details, directory structure, credentials location, network configuration, SSL setup, and security configuration.

### Available Scripts

All scripts are located in `scripts/` and are executable:

1. **init_debian_server.sh** - Setup completo de servidor Debian 12 desde cero
2. **docker_deploy.sh** - Deployment rápido de servicios Docker con templates
3. **ssl_renew.sh** - Renovación de certificado SSL wildcard
4. **backup_mysql.sh** - Backup automatizado de bases de datos MySQL
5. **unban_ip.sh** - Recuperación de acceso SSH (desbanear fail2ban)
6. **container_health.sh** - Monitoreo y diagnóstico de contenedores Docker

### Available References

Detailed documentation in `references/`:

1. **infrastructure.md** - Documentación completa de la infraestructura actual
2. **nginx_patterns.md** - Configuraciones Nginx probadas para diferentes casos
3. **docker_patterns.md** - Templates docker-compose para diferentes servicios
4. **troubleshooting.md** - Guía completa de resolución de problemas

## When to Use Each Resource

### Use Scripts When

- **init_debian_server.sh**: Setting up a new Contabo VPS from scratch
- **docker_deploy.sh**: Deploying new WordPress, n8n, Next.js, or custom services
- **ssl_renew.sh**: SSL certificate is expiring (every 90 days)
- **backup_mysql.sh**: Creating database backups (manually or via cron)
- **unban_ip.sh**: SSH access blocked by fail2ban or other access issues
- **container_health.sh**: Diagnosing container issues or checking system health

### Read References When

- **infrastructure.md**: Before ANY work on the server - contains critical paths and conventions
- **nginx_patterns.md**: Configuring reverse proxy for new services
- **docker_patterns.md**: Creating docker-compose.yml files for new deployments
- **troubleshooting.md**: Diagnosing issues (502 errors, connectivity, disk space, etc.)

## Common Workflows

### 1. Setup New Debian Server

Transfer script to server and run initialization. This installs Docker, Nginx, fail2ban, UFW, certbot, creates directory structure, and applies security hardening.

### 2. Deploy New Service

Read docker patterns for the service type, use deployment script to create docker-compose.yml, configure Nginx reverse proxy using nginx patterns, and test configuration.

### 3. Troubleshoot Access Issues

Run unban script to clear fail2ban blocks. If still failing, read troubleshooting guide for SSH-specific solutions.

### 4. Monitor Container Health

Run container_health.sh for interactive monitoring with resource usage, container status, logs viewing, network inspection, and disk usage analysis.

### 5. Renew SSL Certificate

Run ssl_renew.sh which handles DNS challenge with Cloudflare automatically. Required every 90 days.

### 6. Backup Databases

Run backup_mysql.sh to create compressed backups with 30-day retention in `/opt/pathfinders/backups/mysql/`.

## Critical Conventions

### Always Follow These Rules

1. **Network:** All services MUST use `pathfinders` network (external: true)
2. **Credentials:** Load with `source /opt/pathfinders/.credentials` before starting services
3. **MySQL Host:** Always use `mysql` as the container name/hostname
4. **Directory Structure:** All services under `/opt/pathfinders/<service-name>/`
5. **Nginx Configs:** One file per domain in `/etc/nginx/conf.d/`
6. **Service Order:** Start MySQL BEFORE dependent services
7. **SSL:** Use wildcard cert at `/etc/letsencrypt/live/internationalpathfinders.com/`

## Decision Tree for Common Tasks

### User asks about server setup
Read infrastructure.md to understand current state. If new server: use init_debian_server.sh. If existing: provide commands based on infrastructure.md.

### User asks to deploy a service
Read docker_patterns.md for service type, use docker_deploy.sh or provide manual docker-compose, read nginx_patterns.md for reverse proxy config, provide complete deployment steps.

### User has connectivity/access issues
Run unban_ip.sh if SSH related, read troubleshooting.md for specific error, provide diagnostic commands and solutions.

### User asks about SSL
Check if renewal needed with ssl_renew.sh, verify cert paths in nginx configs, reference nginx_patterns.md for SSL blocks.

### User needs backups
Use backup_mysql.sh for databases, provide tar commands for volumes, reference infrastructure.md for backup location.

### User has container issues
Run container_health.sh for diagnosis, check docker_patterns.md for proper configuration, use troubleshooting.md for specific errors.

### User asks about monitoring
Run container_health.sh, provide docker stats, df -h, free -h commands, check troubleshooting.md for resource issues.

## Response Guidelines

### For setup/deployment tasks:
Read relevant reference files, provide step-by-step commands, explain what each step does, show expected output, include verification commands.

### For troubleshooting:
Acknowledge the issue, provide diagnostic commands first, read troubleshooting.md for solutions, explain root cause, provide prevention tips.

### For configuration:
Read appropriate patterns file, provide complete working config, explain critical sections, include test commands (nginx -t, docker-compose config), show reload/restart commands.

### Always Include

Commands ready to copy-paste, expected output or what to look for, how to verify success, what to do if it fails, links to reference files for more details.

### Language Preference

User communicates primarily in Spanish. Respond in Spanish when appropriate, but keep technical commands and code in English as per standard DevOps practices.

## Maintenance Reminders

- **SSL Renewal:** Every 90 days - use ssl_renew.sh
- **Backups:** Weekly recommended - use backup_mysql.sh
- **Disk Space:** Monitor with df -h and docker system df
- **Security Updates:** Monthly apt update && apt upgrade
- **Log Rotation:** Clean old logs with journalctl --vacuum-time=7d
- **Docker Cleanup:** Monthly docker system prune -a

## Emergency Procedures

### Complete SSH Lockout
Access Contabo panel, enable rescue mode, mount disk and diagnose, fix issue and reboot.

### Server Not Responding
Check Contabo panel for server status, reboot from panel if necessary, wait 2-3 minutes for services to start, verify services.

### Critical Disk Space
Run docker system prune with caution, clean old backups, clean logs with journalctl.

## Additional Resources

- Contabo Panel: https://my.contabo.com/
- Cloudflare Dashboard for DNS and API tokens
- Server IP: 173.212.247.69
- Main Domain: internationalpathfinders.com

---

*This skill embodies 15+ years of DevOps experience with a strong KISS mindset for production-ready, maintainable infrastructure.*
