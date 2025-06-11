# ZEST Project

A microservice-based asynchronous task processing system with FastAPI, Redis, Prometheus, and Pushgateway.

---

## Features

- **FastAPI** REST API for task submission and statistics
- **Worker pool** with configurable concurrency
- **Redis**-backed queue (priority or FIFO)
- **Pluggable metrics**: Redis or Prometheus Pushgateway
- **Prometheus** monitoring and `/metrics` endpoint
- **Centralized logging** with file locking
- **Docker Compose** for easy deployment

---

## Getting Started

### 1. **Clone the repository**

```sh
git clone https://github.com/eliaLaniado/zest-app.git
cd zest-app
```

### 2. **Configure environment**

Edit `.env` as needed (see sample in repo).

### 3. **Build and start with Docker Compose**

```sh
docker-compose up --build
```

This will start:

- API server (FastAPI) on [http://localhost:8000](http://localhost:8000)
- Worker service
- Redis
- Prometheus ([http://localhost:9090](http://localhost:9090))
- Pushgateway ([http://localhost:9091](http://localhost:9091))

---

## Usage

### **Submit tasks**

You can use the provided script to load test:

```sh
bash scripts/load_test_tasks.sh
```

Or submit a single task with `curl`:

```sh
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, world!"}'
```

### **Check statistics**

```sh
curl http://localhost:8000/api/statistics
```

Example response:

```json
{
  "tasks_processed": 10,
  "tasks_retried": 2,
  "tasks_succeeded": 8,
  "tasks_failed": 2,
  "queue_length": 0,
  "idle_workers": 4,
  "active_workers": 0,
  "source": "pushgateway"
}
```

### **Prometheus Metrics**

- Visit [http://localhost:9090](http://localhost:9090) for Prometheus UI.
- Visit [http://localhost:9091](http://localhost:9091) for Pushgateway UI.
- API `/metrics` endpoint: [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## Development

- Install Poetry: https://python-poetry.org/docs/#installation
- Install dependencies:  
  poetry install
- Run API locally:
  ```sh
  uvicorn app.main:app --reload
  ```
- Run worker locally:
  ```sh
  python app/worker.py
  ```

---

## Project Structure

```
app/
  api/           # FastAPI routers
  core/          # Core abstractions and factories
  infrastructure/# Redis, Prometheus, logging implementations
  models/        # Pydantic models
  worker/        # Worker manager and processor
docker/          # Dockerfiles
scripts/         # Utility scripts
```

---

## Author

Eliya laniado
