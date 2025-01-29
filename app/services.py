import requests
from loguru import logger

from app.models import FinancesMetrics
from app.config import TIMEWEB_CLOUD_API_URL


class TimewebAccount:
    token = ''

    def __init__(self, token):
        self.token = token

    def fetch_finances_metrics(self) -> FinancesMetrics:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        try:
            response = requests.get(f"{TIMEWEB_CLOUD_API_URL}/account/finances", headers=headers)
            response.raise_for_status()
            data = response.json().get('finances', {})
            logger.debug(f'{data=}')
        except requests.RequestException as e:
            data = {'fetch_failed': True}
            logger.error(f'Error fetching finances data: {e}')
        logger.debug(f'{data=}')
        return FinancesMetrics(**data)
