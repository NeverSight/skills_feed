---
name: ansible
description: Create, update, or run Ansible playbooks and inventory in this repo for multi-node changes (ansible/). Use for node bootstrap, package installs, or cluster-wide config updates.
---

# Ansible

## Overview

Use Ansible for repeatable, idempotent changes across nodes. Keep playbooks minimal, explicit about hosts, and safe to re-run.

## When to use

- You need to apply the same change on multiple hosts.
- The change touches OS packages, services, or system config.
- You are bootstrapping or maintaining k3s, Rancher, or Tailscale on nodes.

## Inventory and groups

Inventory lives in `ansible/inventory/hosts.ini`. Common groups:

- `kube_masters` (k3s masters)
- `kube_workers` (k3s workers)
- `k3s_cluster` (masters + workers)
- `proxy` (nuc)
- `docker_hosts` (docker-host)

## Quick start

Ping all nodes in the cluster:

```bash
ansible -i ansible/inventory/hosts.ini k3s_cluster -m ping -u kalmyk
```

Run a playbook on all nodes in the cluster:

```bash
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/install_nfs_client.yml -u kalmyk -b
```

Limit to a single host:

```bash
ansible-playbook -i ansible/inventory/hosts.ini ansible/playbooks/install_tailscale.yml -u kalmyk -b --limit kube-worker-00
```

## Common playbooks in this repo

- `install_nfs_client.yml` - install NFS client tools on nodes
- `install_tailscale.yml` - install Tailscale packages
- `start_enable_tailscale.yml` - enable and start tailscaled
- `start_enable_tailscale_client.yml` - start Tailscale client services
- `k3s-ha.yml` - configure k3s HA cluster
- `k3s-oidc.yml` - configure OIDC for k3s
- `rancher2.yml` - install Rancher
- `wait_for_rancher.yml` - wait until Rancher is ready
- `rancher_bootstrap_logs.yml` - capture Rancher bootstrap logs
- `start_rancher2_container.yml` - start Rancher container

## Safety and idempotency

- Prefer Ansible modules over shell commands.
- Use `--check` and `--diff` when validating a risky change.
- Use `--limit` to scope changes during testing.
- Keep playbooks idempotent so re-runs are safe.

## Validation

- Service check: `systemctl status tailscaled`
- Logs: `journalctl -u tailscaled --no-pager -n 50`
- Cluster check: `kubectl get nodes -o wide`

## Resources

- Reference: `references/ansible-runbook.md`
- Runner: `scripts/run-playbook.sh`
- Template: `assets/playbook-template.yml`
