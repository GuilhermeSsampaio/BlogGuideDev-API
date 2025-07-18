import secrets

# Gerar chave aleatória de 32 bytes (256 bits)
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")