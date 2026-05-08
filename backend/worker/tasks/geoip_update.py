from worker.celery_app import ONCE_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.geoip_update.run", **ONCE_TASK_OPTS)
def run() -> None:
    # TODO: download latest GeoLite2-City.mmdb from MaxMind
    pass
