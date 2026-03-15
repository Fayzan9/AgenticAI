# Base Python image
FROM python:3.11-slim

# Install system dependencies + Node.js (required for Codex CLI)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Codex CLI globally
RUN npm install -g @openai/codex

# Optional: verify installation
RUN codex --version || true

# Create workspace directory
WORKDIR /workspace

# Copy entrypoint
COPY entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

# Set entrypoint
ENTRYPOINT ["python3", "/app/entrypoint.py"]