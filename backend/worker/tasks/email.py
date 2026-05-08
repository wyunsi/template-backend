from worker.celery_app import RETRY_TASK_OPTS, celery_app


@celery_app.task(name="worker.tasks.email.send", **RETRY_TASK_OPTS)
def send(to: str, subject: str, html: str) -> None:
    # TODO: implement via resend SDK
    raise NotImplementedError
