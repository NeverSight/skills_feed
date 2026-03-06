---
name: network
description: Debug network connectivity, configure load balancers, and analyze traffic. Use for connectivity issues, network optimization, or protocol debugging.
---

# Network Engineering

Debug connectivity and configure network infrastructure.

## When to use

- Connectivity issues
- Load balancer setup
- SSL/TLS problems
- DNS debugging
- Network performance

## Diagnostic commands

### Connectivity testing

```bash
# Basic connectivity
ping -c 4 host.example.com
traceroute host.example.com

# Port check
nc -zv host.example.com 443
telnet host.example.com 80

# DNS lookup
dig +short example.com
dig +trace example.com
nslookup -type=MX example.com

# HTTP testing
curl -v https://api.example.com/health
curl -w "@curl-format.txt" -o /dev/null -s https://example.com
```

### curl-format.txt

```
     time_namelookup:  %{time_namelookup}s\n
        time_connect:  %{time_connect}s\n
     time_appconnect:  %{time_appconnect}s\n
    time_pretransfer:  %{time_pretransfer}s\n
       time_redirect:  %{time_redirect}s\n
  time_starttransfer:  %{time_starttransfer}s\n
                     ----------\n
          time_total:  %{time_total}s\n
```

### SSL/TLS debugging

```bash
# Check certificate
openssl s_client -connect example.com:443 -servername example.com

# Verify certificate chain
openssl s_client -connect example.com:443 -showcerts

# Check expiry
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Test specific TLS version
curl --tlsv1.2 --tls-max 1.2 https://example.com
```

## Load balancer config

### Nginx

```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080 weight=5;
    server backend2.example.com:8080 weight=3;
    server backend3.example.com:8080 backup;

    keepalive 32;
}

server {
    listen 443 ssl http2;
    server_name api.example.com;

    ssl_certificate /etc/ssl/certs/api.crt;
    ssl_certificate_key /etc/ssl/private/api.key;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_connect_timeout 5s;
        proxy_read_timeout 60s;
    }

    location /health {
        access_log off;
        return 200 "OK";
    }
}
```

## Traffic analysis

```bash
# Capture packets
tcpdump -i eth0 -w capture.pcap port 443

# Read capture
tcpdump -r capture.pcap -n

# Filter by host
tcpdump -i any host 10.0.0.1 and port 80

# Show HTTP requests
tcpdump -i any -A -s 0 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

## Common issues

| Symptom            | Check                       | Fix                               |
| ------------------ | --------------------------- | --------------------------------- |
| Connection refused | Port open? Service running? | Start service, open firewall      |
| Connection timeout | Firewall? Route?            | Check security groups, routing    |
| SSL error          | Cert valid? Chain complete? | Renew cert, fix chain             |
| DNS failure        | Resolver? Record exists?    | Check DNS config, add record      |
| Slow response      | Latency? Bandwidth?         | Optimize route, increase capacity |

## Examples

**Input:** "API calls timing out"
**Action:** Test connectivity, check DNS, verify SSL, analyze latency

**Input:** "Set up load balancer"
**Action:** Configure nginx/HAProxy, add health checks, test failover
