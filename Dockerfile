ARG PYTHON_VERSION=3.13

# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project into `/app`
WORKDIR /app

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Then, use a final image without uv (NOTE: uv uses "bookworm-slim" and Python uses "slim-bookworm")
FROM python:${PYTHON_VERSION}-slim-bookworm

# Copy the application from the builder
COPY --from=builder --chown=app:app /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Set the working directory to the application
WORKDIR /app

# Set ENV variable defaults
ENV ENVIRONMENT=production

# Run the FastAPI application by default
CMD ["fastapi", "run", "app/core.py", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]