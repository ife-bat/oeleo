# How to test oeleo

## Unit tests

Run the default unit test suite:

```bash
uv run pytest
```


## SSH integration tests

These tests are skipped by default. They require a real SSH server.

### Quick start with Docker (recommended)

1) Start a disposable SSH server:

```bash
docker run -d --name oeleo-ssh -p 2222:2222 \
  -e USER_NAME=oeleo \
  -e USER_PASSWORD=oeleo \
  -e PASSWORD_ACCESS=true \
  linuxserver/openssh-server:latest
```

Or with docker compose:

```bash
docker compose up -d
```

2) Set env vars (PowerShell):

```powershell
$env:OELEO_SSH_TESTS="1"
$env:OELEO_USERNAME="oeleo"
$env:OELEO_EXTERNAL_HOST="localhost:2222"
$env:OELEO_PASSWORD="oeleo"
```

Git Bash (bash):

```bash
export OELEO_SSH_TESTS=1
export OELEO_USERNAME=oeleo
export OELEO_EXTERNAL_HOST=localhost:2222
export OELEO_PASSWORD=oeleo
```

If you prefer a script, use the repo-root `set-ssh-env.sh` and source it
so the variables persist in your shell:

```bash
source ../set-ssh-env.sh
uv run pytest -m ssh
```

From the repo root, you can also do:

```bash
source ./set-ssh-env.sh
uv run pytest -m ssh
```

3) Run only SSH tests:

```bash
uv run pytest -m ssh
```

### Notes

- The tests use password auth and assume a POSIX shell on the server.
- `SSHConnector` requires `OELEO_PASSWORD` even if you plan to use keys.
- If your Fabric setup does not accept `host:port`, map the container to port 22
  or configure an SSH host entry in `~/.ssh/config`.

### Useful Docker commands

```bash
# Tail container logs
docker logs -f oeleo-ssh

# List containers
docker ps
docker ps -a

# SSH into the container (password: oeleo)
ssh -p 2222 oeleo@localhost

# Stop/start the container
docker stop oeleo-ssh
docker start oeleo-ssh

# Remove the container
docker rm -f oeleo-ssh

# Stop and remove via compose
docker compose down
```
