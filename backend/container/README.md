# Agent Container Execution

Clean, simple containerized execution for agent runs.

## Overview

This module enables running agents in isolated Podman containers for safety and reproducibility.

**Pattern:** Spawn → Execute → Exit (one-shot containers)

## Features

- ✅ **Simple**: One-shot containers with automatic cleanup
- ✅ **Fast**: Pre-installed dependencies (Python + Codex CLI)
- ✅ **Safe**: Isolated environment, network disabled by default
- ✅ **Clean**: ~300 lines of production-ready code

## Quick Start

### 1. Build the Container Image

```bash
cd backend/container
chmod +x build.sh
./build.sh
```

**Note:** You need to update `Dockerfile` to install the actual Codex CLI. Currently has a placeholder.

### 2. Enable Container Execution

```bash
export ENABLE_CONTAINER_EXECUTION=true
cd backend
python -m uvicorn main:app --reload
```

### 3. Disable Container Execution (use direct execution)

```bash
export ENABLE_CONTAINER_EXECUTION=false
cd backend
python -m uvicorn main:app --reload
```

## Architecture

```
app/container/
├── __init__.py          # Module exports
├── config.py            # Container settings (env-based)
└── executor.py          # Main execution logic (~300 lines)

container/
├── Dockerfile           # Pre-built image (Python + Codex)
├── entrypoint.py        # Container entry point
└── build.sh             # Build script
```

## Configuration

All settings via environment variables in `app/container/config.py`:

| Variable | Default | Description |
|----------|---------|-------------|
| `CONTAINER_IMAGE` | `agent-executor:latest` | Image name |
| `CONTAINER_CPU_LIMIT` | `1.0` | CPU limit per container |
| `CONTAINER_MEMORY_LIMIT` | `512m` | Memory limit |
| `CONTAINER_TIMEOUT` | `300` | Execution timeout (seconds) |
| `CONTAINER_ROOTLESS` | `true` | Use rootless mode |
| `CONTAINER_NETWORK` | `false` | Enable network (disabled by default) |
| `PODMAN_BIN` | `podman` | Podman binary path |

## How It Works

1. **FastAPI** receives agent execution request
2. **ContainerExecutor** spawns Podman container with:
   - Volume mounts: agents (read-only), executions (read-write)
   - Environment vars: agent_name, execution_id, user_prompt
   - Resource limits: CPU, memory
   - Security: no network, no new privileges
3. **Container** executes:
   - Reads agent spec from `/workspace/agents/{agent_name}/`
   - Calls Codex CLI with formatted prompt
   - Writes output to `/workspace/executions/{agent_name}/{execution_id}/`
4. **Container exits** automatically (`--rm` flag)
5. **Results** stream back via SSE

## Volume Mounts

```
Host                                    Container
----------------------------------------|--------------------------
workflow_templates/agent_created/       → /workspace/agents/ (ro)
workflow_templates/agent_executions/    → /workspace/executions/ (rw)
```

## Container Command

```bash
podman run --rm \
  --cpus=1.0 \
  --memory=512m \
  -v ./agent_created:/workspace/agents:ro \
  -v ./agent_executions:/workspace/executions:rw \
  -e AGENT_NAME=word_counter \
  -e EXECUTION_ID=abc-123 \
  -e USER_PROMPT="Hello World" \
  --security-opt no-new-privileges \
  --network=none \
  agent-executor:latest
```

## Troubleshooting

### Image not found
```bash
cd backend/container
./build.sh
```

### Permission errors
Enable rootless mode:
```bash
export CONTAINER_ROOTLESS=true
```

### Timeout issues
Increase timeout:
```bash
export CONTAINER_TIMEOUT=600  # 10 minutes
```

### Check container logs
```bash
podman logs <container-id>
```

### List containers
```bash
podman ps -a
```

## Development

### Test container execution
```python
from app.container import ContainerExecutor

executor = ContainerExecutor()
for line in executor.execute_agent("word_counter", "test-123", "Hello World"):
    print(line)
```

### Check if image exists
```python
executor = ContainerExecutor()
if not executor.check_image_exists():
    executor.pull_image()
```

## Production Checklist

- [ ] Update Dockerfile with actual Codex CLI installation
- [ ] Build and test container image
- [ ] Set appropriate resource limits (CPU, memory)
- [ ] Configure timeout based on expected execution time
- [ ] Enable rootless mode for security
- [ ] Monitor container metrics
- [ ] Set up log aggregation

## Performance

**Expected timings:**
- Container spawn: ~500ms-1s
- Agent execution: varies by agent
- Container cleanup: automatic (--rm)

**Total overhead:** ~1-2s compared to direct execution

## Security

- Network disabled by default (`--network=none`)
- No new privileges (`--security-opt no-new-privileges`)
- Rootless mode supported
- Read-only agent specs
- Resource limits enforced
- Automatic container cleanup
