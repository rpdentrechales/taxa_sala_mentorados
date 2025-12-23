FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# deps do sistema (mínimo)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Cloud Run usa a env PORT
CMD ["bash", "-lc", "streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true"]
