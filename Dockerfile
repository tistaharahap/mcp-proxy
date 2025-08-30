FROM python:3.11-slim

# Install uv by copying from the official Docker image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

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