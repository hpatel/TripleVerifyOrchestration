# -------- Base --------
FROM python:3.11-slim

# Install uv (Rust-based pip replacement)
RUN pip install --no-cache-dir uv

WORKDIR /app

# -------- Dependency layer (cached) --------
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache \
    uv pip install --system -r requirements.txt

# -------- App layer --------
COPY . .

# -------- Run --------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]