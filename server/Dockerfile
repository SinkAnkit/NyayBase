FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 7860

# Run with gunicorn — use $PORT from platform, default 7860 (HuggingFace Spaces)
CMD gunicorn main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-7860} --workers 1 --timeout 120
