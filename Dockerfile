FROM python:3.11-slim

WORKDIR /app

# System deps (optional but safe for uvicorn extras)
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY pyproject.toml pytest.ini README.md ./
COPY docs ./docs

EXPOSE 8000

ENV APP_ENV=production
ENV LOG_LEVEL=INFO

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
