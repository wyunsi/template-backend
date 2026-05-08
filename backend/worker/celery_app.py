"""
Celery application entry point.

autodiscover_tasks is NOT used because core/license/ and core/security/
are compiled to .so by Cython — Celery cannot autodiscover tasks
inside compiled packages. All task modules must be listed explicitly.
"""

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from core.config import settings

celery_app = Celery("api")

celery_app.conf.update(
    broker_url=settings.celery.broker_url,
    result_backend=settings.celery.result_backend,
    task_serializer=settings.celery.task_serializer,
    result_serializer=settings.celery.result_serializer,
    accept_content=["json"],
    timezone=settings.celery.timezone,
    enable_utc=True,
    # Queue routing
    task_routes={
        "worker.tasks.email.*": {"queue": "notify"},
        "worker.tasks.event_dispatch.*": {"queue": "notify"},
        "worker.tasks.outbox_dispatcher.*": {"queue": "maintenance"},
        "worker.tasks.backup.*": {"queue": "maintenance"},
        "worker.tasks.cleanup.*": {"queue": "maintenance"},
        "worker.tasks.geoip_update.*": {"queue": "maintenance"},
        "worker.tasks.key_rotation.*": {"queue": "maintenance"},
    },
    task_default_queue="notify",
    # Explicit task include list (required when Cython compiles core/)
    include=[
        "worker.tasks.email",
        "worker.tasks.event_dispatch",
        "worker.tasks.outbox_dispatcher",
        "worker.tasks.backup",
        "worker.tasks.cleanup",
        "worker.tasks.geoip_update",
        "worker.tasks.key_rotation",
    ],
    # Beat schedule
    beat_schedule={
        "outbox-poll": {
            "task": "worker.tasks.outbox_dispatcher.poll",
            "schedule": settings.celery.outbox_poll_interval,
        },
        "daily-backup": {
            "task": "worker.tasks.backup.run",
            "schedule": 86400,
        },
        "daily-cleanup": {
            "task": "worker.tasks.cleanup.run",
            "schedule": 86400,
        },
        "weekly-geoip-update": {
            "task": "worker.tasks.geoip_update.run",
            "schedule": 7 * 86400,
        },
    },
)

# Default retry template for notify-queue tasks
RETRY_TASK_OPTS = {
    "autoretry_for": (Exception,),
    "max_retries": 3,
    "retry_backoff": True,
    "retry_backoff_max": 300,
    "retry_jitter": True,
}

# One-shot template for maintenance tasks (no retry, log on failure)
ONCE_TASK_OPTS = {
    "autoretry_for": (),
    "max_retries": 0,
}


@worker_process_init.connect
def init_worker(**kwargs) -> None:
    from core.database.sync_ import init_sync_engine
    init_sync_engine()


@worker_process_shutdown.connect
def shutdown_worker(**kwargs) -> None:
    from core.database.sync_ import dispose_sync_engine
    dispose_sync_engine()
