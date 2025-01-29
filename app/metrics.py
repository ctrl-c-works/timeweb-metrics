import asyncio

from prometheus_client import Gauge, generate_latest
from loguru import logger

from app.services import TimewebAccount
from app.config import ACCOUNTS, SCRAPE_INTERVAL
from app.models import FinancesMetrics


class MetricsCollector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MetricsCollector, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.metrics = {}
            self._initialize_metrics()
            self.initialized = True

    def _initialize_metrics(self):
        # Используем атрибуты FinancesMetrics
        for field_name, field in FinancesMetrics.model_fields.items():
            description = field.description or f"Metric for {field_name.replace('_', ' ')}"
            gauge_name = f"timeweb_finances_{field_name}"
            self.metrics[field_name] = Gauge(gauge_name, description, ['account'])

    async def update_metrics(self):
        while True:
            for account in ACCOUNTS:
                try:
                    logger.debug(f'Updating metrics for account "{account["name"]}"')
                    timeweb_account = TimewebAccount(account['token'])
                    finances_metrics = timeweb_account.fetch_finances_metrics()
                    logger.debug(f'{finances_metrics=}')
                    # Обновляем метрики для аккаунта
                    for field_name, gauge in self.metrics.items():
                        value = getattr(finances_metrics, field_name, None)
                        gauge.labels(account['name']).set(value)
                except Exception as e:
                    logger.error(f"Unexpected error for {account['name']}: {str(e)}")
            # Интервал обновления данных
            await asyncio.sleep(SCRAPE_INTERVAL)

    @staticmethod
    def get_latest_metrics():
        return generate_latest()
