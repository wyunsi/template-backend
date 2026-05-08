from worker.celery_app import RETRY_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.event_dispatch.dispatch", **RETRY_TASK_OPTS)
def dispatch(event_id: int) -> None:
    # TODO: deliver outbox event to external webhook
    raise NotImplementedError
