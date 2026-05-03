ALTER TABLE comentario
ADD COLUMN IF NOT EXISTS parent_id UUID NULL;

CREATE INDEX IF NOT EXISTS idx_comentario_parent_id
ON comentario(parent_id);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.table_constraints
        WHERE constraint_name = 'fk_comentario_parent_id'
          AND table_name = 'comentario'
    ) THEN
        ALTER TABLE comentario
        ADD CONSTRAINT fk_comentario_parent_id
        FOREIGN KEY (parent_id)
        REFERENCES comentario(id)
        ON DELETE CASCADE;
    END IF;
END $$;