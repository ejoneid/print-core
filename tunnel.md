# SSH Tunnel Notes

This document describes how the reverse SSH tunnel is configured and what SSH server settings are required so containers can reach the tunneled port.

## What the tunnel does

The code in `print_core/tunnel.py` opens a **reverse** SSH tunnel:

- **Remote (host) port:** `19001`
- **Local port:** `18000`

Conceptually:

```
remote host (docker host) :19001  -->  local machine :18000
```

The tunnel is created with:
- `remote_bind_host="0.0.0.0"` (so it should listen on all interfaces)
- `local_bind_host="127.0.0.1"` (local service is loopback-only)

## Required SSH server settings (Ubuntu)

On the **docker host**, edit:

`/etc/ssh/sshd_config`

Ensure these are set (globally or in the relevant `Match` block):

```
GatewayPorts clientspecified
AllowTcpForwarding yes
```

`GatewayPorts clientspecified` allows the client (the tunnel code) to request `0.0.0.0` for the remote bind. Without this, OpenSSH defaults to binding the reverse tunnel on `127.0.0.1`, which is **not reachable** from containers.

## Restart SSH

```bash
sudo systemctl restart ssh
```

## Verify the bind

```bash
ss -ltnp | grep 19001
```

Expected output should show:

- `0.0.0.0:19001` (and/or `[::]:19001`)

If you only see `127.0.0.1:19001`, then `GatewayPorts` is still not effective (often due to a `Match` block overriding it).

## Access from containers

From a container on the Docker bridge network, use:

```
http://host.docker.internal:19001
```

Or use the bridge gateway IP directly (e.g., `http://172.17.0.1:19001`) if `host.docker.internal` is not mapped.
