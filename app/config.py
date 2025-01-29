from dynaconf import Dynaconf


settings = Dynaconf(
    settings_files=['config.yaml', '/config/config.yaml'],
)

SENTRY_DSN = settings.sentry_dsn

TIMEWEB_CLOUD_API_URL = settings.timeweb_cloud_api_url
ACCOUNTS = settings.accounts
SCRAPE_INTERVAL = settings.scrape_interval
