from pydantic import BaseModel, ConfigDict, Field


class PushSubscriptionKeys(BaseModel):
    p256dh: str
    auth: str


class PushSubscriptionIn(BaseModel):
    endpoint: str
    expiration_time: float | None = Field(default=None, alias="expirationTime")
    keys: PushSubscriptionKeys

    model_config = ConfigDict(populate_by_name=True)


class PushUnsubscribeRequest(BaseModel):
    endpoint: str


class PushPublicKeyResponse(BaseModel):
    public_key: str


class PushSubscribeResponse(BaseModel):
    success: bool
