import json
import logging
import threading
from typing import Iterable
from uuid import UUID

from pywebpush import WebPushException, webpush
from sqlmodel import Session

from config.db import engine
from config.settings import FRONTEND_URL, VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY, VAPID_SUBJECT
from models.push_subscription import PushSubscription
from repository.push_subscription_crud import (
    list_all_push_subscriptions,
    list_push_subscriptions_for_user,
    remove_push_subscription,
)

logger = logging.getLogger(__name__)


def is_push_configured() -> bool:
    return bool(VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY and VAPID_SUBJECT)


def resolve_reference_path(tipo_referencia: str, referencia_id: str) -> str:
    if tipo_referencia == "forum":
        return f"/forum/{referencia_id}"
    if tipo_referencia in ("post", "conteudo"):
        return f"/conteudo/{referencia_id}"
    if tipo_referencia == "vaga":
        return f"/vagas/{referencia_id}"
    return "/"


def build_app_url(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    base = FRONTEND_URL.rstrip("/")
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base}{path}"


def build_push_payload(
    title: str,
    body: str,
    url: str,
    tag: str | None = None,
    icon: str | None = None,
    badge: str | None = None,
) -> str:
    payload = {
        "title": title,
        "body": body,
        "url": build_app_url(url),
    }
    if tag:
        payload["tag"] = tag
    if icon:
        payload["icon"] = icon
    if badge:
        payload["badge"] = badge
    return json.dumps(payload)


def _send_payload_to_subscriptions(
    session: Session,
    subscriptions: Iterable[PushSubscription],
    payload: str,
) -> int:
    if not is_push_configured():
        logger.info("Push notifications are not configured.")
        return 0

    sent = 0
    for subscription in subscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": subscription.endpoint,
                    "keys": {
                        "p256dh": subscription.p256dh,
                        "auth": subscription.auth,
                    },
                },
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims={"sub": VAPID_SUBJECT},
            )
            sent += 1
        except WebPushException as exc:
            status_code = getattr(exc.response, "status_code", None)
            if status_code in (404, 410):
                remove_push_subscription(session, subscription.endpoint)
            logger.warning("Push send failed: %s", exc)
        except Exception as exc:
            logger.warning("Push send error: %s", exc)

    return sent


def send_push_to_user(session: Session, destinatario_id: UUID, payload: str) -> int:
    subscriptions = list_push_subscriptions_for_user(session, destinatario_id)
    return _send_payload_to_subscriptions(session, subscriptions, payload)


def send_push_broadcast(
    session: Session,
    payload: str,
    exclude_user_id: UUID | None = None,
) -> int:
    subscriptions = list_all_push_subscriptions(session, exclude_user_id)
    return _send_payload_to_subscriptions(session, subscriptions, payload)


def queue_push_to_user(destinatario_id: UUID, payload: str) -> None:
    if not is_push_configured():
        return

    def _task() -> None:
        with Session(engine) as session:
            send_push_to_user(session, destinatario_id, payload)

    threading.Thread(target=_task, daemon=True).start()


def queue_push_broadcast(payload: str, exclude_user_id: UUID | None = None) -> None:
    if not is_push_configured():
        return

    def _task() -> None:
        with Session(engine) as session:
            send_push_broadcast(session, payload, exclude_user_id)

    threading.Thread(target=_task, daemon=True).start()
