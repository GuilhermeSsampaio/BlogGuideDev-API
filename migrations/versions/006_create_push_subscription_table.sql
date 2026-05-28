CREATE TABLE IF NOT EXISTS push_subscription (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    endpoint TEXT NOT NULL,
    p256dh TEXT NOT NULL,
    auth TEXT NOT NULL,
    expiration_time DOUBLE PRECISION NULL,
    user_agent TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_push_subscription_user FOREIGN KEY (user_id) REFERENCES blogguideuser(id)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_push_subscription_endpoint ON push_subscription(endpoint);
CREATE INDEX IF NOT EXISTS idx_push_subscription_user ON push_subscription(user_id);
