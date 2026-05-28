from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlmodel import Session, select

from models.push_subscription import PushSubscription


def upsert_push_subscription(
    session: Session,
    user_id: UUID,
    endpoint: str,
    p256dh: str,
    auth: str,
    expiration_time: float | None,
    user_agent: str | None = None,
) -> PushSubscription:
    subscription = session.exec(
        select(PushSubscription).where(PushSubscription.endpoint == endpoint)
    ).first()
    now = datetime.now(timezone.utc)

    if subscription:
        subscription.user_id = user_id
        subscription.p256dh = p256dh
        subscription.auth = auth
        subscription.expiration_time = expiration_time
        subscription.user_agent = user_agent
        subscription.updated_at = now
    else:
        subscription = PushSubscription(
            user_id=user_id,
            endpoint=endpoint,
            p256dh=p256dh,
            auth=auth,
            expiration_time=expiration_time,
            user_agent=user_agent,
            created_at=now,
            updated_at=now,
        )

    session.add(subscription)
    session.commit()
    session.refresh(subscription)
    return subscription


def remove_push_subscription(
    session: Session,
    endpoint: str,
    user_id: UUID | None = None,
) -> bool:
    query = select(PushSubscription).where(PushSubscription.endpoint == endpoint)
    if user_id:
        query = query.where(PushSubscription.user_id == user_id)
    subscription = session.exec(query).first()
    if not subscription:
        return False
    session.delete(subscription)
    session.commit()
    return True


def list_push_subscriptions_for_user(
    session: Session,
    user_id: UUID,
) -> List[PushSubscription]:
    return session.exec(
        select(PushSubscription).where(PushSubscription.user_id == user_id)
    ).all()


def list_all_push_subscriptions(
    session: Session,
    exclude_user_id: UUID | None = None,
) -> List[PushSubscription]:
    query = select(PushSubscription)
    if exclude_user_id:
        query = query.where(PushSubscription.user_id != exclude_user_id)
    return session.exec(query).all()
