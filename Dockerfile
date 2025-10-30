# ============================
# Stage 1 — Base image
# ============================
FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ============================
# Stage 2 — Install dependencies
# ============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================
# Stage 3 — Copy project files
# ============================
COPY app ./app

# ============================
# Stage 4 — Use dynamic port
# ============================
EXPOSE 8080

# ============================
# Stage 5 — Launch app (Cloud Run uses $PORT)
# ============================
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --proxy-headers --forwarded-allow-ips='*'"]
