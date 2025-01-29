import asyncio

import sentry_sdk
from fastapi import FastAPI, Response

from app.metrics import MetricsCollector
from app.config import SENTRY_DSN


sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
)

app = FastAPI()

metrics_collector = MetricsCollector()

@app.get("/metrics")
async def get_metrics():
    metrics_data = metrics_collector.get_latest_metrics()
    return Response(content=metrics_data, media_type="text/plain")

@app.get("/health_check")
async def healthcheck():
    return {"status": "healthy"}

# Запуск задачи сбора метрик
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(metrics_collector.update_metrics())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
