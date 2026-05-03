CREATE TABLE IF NOT EXISTS sugestao (
    id UUID PRIMARY KEY,
    user_id UUID NULL,
    tipo VARCHAR(30) NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT NOT NULL,
    email_contato VARCHAR(255) NULL,
    canal_contato VARCHAR(30) NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'aberta',
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sugestao_user FOREIGN KEY (user_id) REFERENCES blogguideuser(id)
);

CREATE INDEX IF NOT EXISTS idx_sugestao_user_id ON sugestao(user_id);
CREATE INDEX IF NOT EXISTS idx_sugestao_tipo ON sugestao(tipo);
CREATE INDEX IF NOT EXISTS idx_sugestao_status ON sugestao(status);