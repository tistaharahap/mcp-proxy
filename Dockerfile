FROM python:3.13-slim

# Install uv by copying from the official Docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy npx from Node.js official image
COPY --from=node:22-slim /usr/local/bin/npx /usr/local/bin/npx
COPY --from=node:22-slim /usr/local/bin/node /usr/local/bin/node
COPY --from=node:22-slim /usr/local/lib/node_modules /usr/local/lib/node_modules

# Copy bunx from Bun official image
COPY --from=oven/bun:1 /usr/local/bin/bunx /usr/local/bin/bunx
COPY --from=oven/bun:1 /usr/local/bin/bun /usr/local/bin/bun

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with caching
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Copy the rest of the application
COPY . .

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Set the PATH to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]