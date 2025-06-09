FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-root

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "app/worker.py"]