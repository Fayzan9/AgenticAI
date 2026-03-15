"""
Container execution configuration.
Simple settings for containerized agent execution.
"""

import os

# Container image (pre-built with Python + Codex CLI)
CONTAINER_IMAGE = os.getenv("CONTAINER_IMAGE", "agent-executor:latest")

# Resource limits
CPU_LIMIT = os.getenv("CONTAINER_CPU_LIMIT", "1.0")
MEMORY_LIMIT = os.getenv("CONTAINER_MEMORY_LIMIT", "512m")

# Execution timeout (seconds)
EXECUTION_TIMEOUT = int(os.getenv("CONTAINER_TIMEOUT", "300"))  # 5 minutes

# Security
ENABLE_ROOTLESS = os.getenv("CONTAINER_ROOTLESS", "true").lower() == "true"
ENABLE_NETWORK = os.getenv("CONTAINER_NETWORK", "true").lower() == "true"  # Enabled by default for Codex CLI API access

# Podman binary
PODMAN_BIN = os.getenv("PODMAN_BIN", "podman")
