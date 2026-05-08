from worker.celery_app import ONCE_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.cleanup.run", **ONCE_TASK_OPTS)
def run() -> None:
    # TODO: purge expired sessions, old audit logs, temp files
    pass
