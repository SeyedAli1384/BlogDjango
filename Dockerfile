# Stage 1: install Python dependencies
FROM python:3.13-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: minimal runtime image
FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Run Django as a non-root user
RUN groupadd --system app \
    && useradd --system --gid app app \
    && mkdir -p /data /app/staticfiles \
    && chown -R app:app /data /app

# Copy installed packages from the builder
COPY --from=builder /install /usr/local

# Copy application source, excluding .dockerignore entries
COPY --chown=app:app . /app

USER app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
