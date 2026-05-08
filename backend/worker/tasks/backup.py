from worker.celery_app import ONCE_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.backup.run", **ONCE_TASK_OPTS)
def run() -> None:
    # TODO: pg_dump + rotate old files
    pass
