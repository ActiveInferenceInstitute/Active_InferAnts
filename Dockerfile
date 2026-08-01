# Active InferAnts — minimal runtime image
FROM python:3.11-slim

WORKDIR /app

# Install Python package + core deps.
COPY pyproject.toml requirements.txt README.md ./
COPY active_infer_ants ./active_infer_ants
COPY 6_API ./6_API

RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -e .

EXPOSE 8000

CMD ["uvicorn", "6_API.Knowledge_API:app", "--host", "0.0.0.0", "--port", "8000"]
