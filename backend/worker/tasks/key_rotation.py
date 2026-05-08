from worker.celery_app import ONCE_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.key_rotation.run", **ONCE_TASK_OPTS)
def run() -> None:
    # TODO: rotate Fernet keys, update SECURITY_FERNET_KEY_OLD
    pass
