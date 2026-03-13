FROM python:3.11-slim

# System deps for tenseal (FHE) build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential cmake && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system cixio && adduser --system --ingroup cixio cixio

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER cixio

EXPOSE 5001

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001/')" || exit 1

CMD ["python", "web_app.py"]
