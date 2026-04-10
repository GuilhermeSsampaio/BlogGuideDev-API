-- Script para adicionar a coluna cnpj na tabela blogguideuser
-- Execute este comando no seu console do banco de dados (MySQL/PostgreSQL)

ALTER TABLE blogguideuser ADD COLUMN cnpj VARCHAR(14) DEFAULT NULL;
