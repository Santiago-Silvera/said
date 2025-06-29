# Docker file for backend 
FROM python:3.12-slim AS base

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# ===================== DEVELOPMENT =====================
FROM base AS development

ENV FLASK_APP=said.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
EXPOSE 5000

USER appuser
CMD ["flask", "run", "--host=0.0.0.0"]

# ===================== PRODUCTION =====================
FROM base AS production

ENV FLASK_APP=said.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=0
EXPOSE 5000

USER appuser
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "said:app"]

