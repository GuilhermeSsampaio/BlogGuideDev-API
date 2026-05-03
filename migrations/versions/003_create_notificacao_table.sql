CREATE TABLE IF NOT EXISTS notificacao (
    id UUID PRIMARY KEY,
    destinatario_id UUID NOT NULL,
    ator_id UUID NULL,
    tipo VARCHAR(50) NOT NULL,
    referencia_id UUID NOT NULL,
    tipo_referencia VARCHAR(50) NOT NULL,
    mensagem TEXT NOT NULL,
    lida BOOLEAN NOT NULL DEFAULT FALSE,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notificacao_destinatario FOREIGN KEY (destinatario_id) REFERENCES blogguideuser(id),
    CONSTRAINT fk_notificacao_ator FOREIGN KEY (ator_id) REFERENCES blogguideuser(id)
);

CREATE INDEX IF NOT EXISTS idx_notificacao_destinatario ON notificacao(destinatario_id);
CREATE INDEX IF NOT EXISTS idx_notificacao_lida ON notificacao(lida);
CREATE INDEX IF NOT EXISTS idx_notificacao_data_criacao ON notificacao(data_criacao);