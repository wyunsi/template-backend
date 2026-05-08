from worker.celery_app import ONCE_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.outbox_dispatcher.poll", **ONCE_TASK_OPTS)
def poll() -> None:
    # TODO: scan outbox table, enqueue pending events via event_dispatch.dispatch
    pass
