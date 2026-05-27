"""
Serviço de envio de e-mail via SMTP (Gmail).

Usa as variáveis de ambiente:
  SMTP_EMAIL    – e-mail remetente (ex: seu-app@gmail.com)
  SMTP_PASSWORD – App Password do Gmail (não a senha normal)

Para gerar uma App Password no Gmail:
  1. Ative a verificação em duas etapas na sua conta Google.
  2. Vá em https://myaccount.google.com/apppasswords
  3. Gere uma senha para "Outro (nome personalizado)" → use "BlogGuide".
  4. Copie a senha de 16 caracteres e coloque em SMTP_PASSWORD no .env.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config.settings import (
    SMTP_EMAIL,
    SMTP_PASSWORD,
    FEEDBACK_RECIPIENT_EMAIL,
)

logger = logging.getLogger(__name__)


def send_feedback_email(
    tipo: str,
    titulo: str,
    descricao: str,
    canal_contato: str | None = None,
    email_contato: str | None = None,
    user_name: str | None = None,
) -> bool:
    """
    Envia um e-mail de feedback/sugestão para o destinatário configurado.
    Retorna True se enviou com sucesso, False caso contrário.
    """
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        logger.warning(
            "SMTP_EMAIL ou SMTP_PASSWORD não configurados. "
            "E-mail de feedback não será enviado."
        )
        return False

    tipo_label = "🐛 Bug" if tipo == "bug" else "💡 Sugestão"
    canal_label = canal_contato or "Não informado"
    contato_label = email_contato or "Não informado"
    user_label = user_name or "Anônimo"

    subject = f"[BlogGuide] {tipo_label}: {titulo}"

    html_body = f"""
    <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8f9fa; border-radius: 12px; overflow: hidden; border: 1px solid #e0e0e0;">
        <div style="background: linear-gradient(135deg, #6c2bd7, #9b59b6); padding: 24px 30px;">
            <h1 style="color: #fff; margin: 0; font-size: 22px;">
                {tipo_label}
            </h1>
            <p style="color: rgba(255,255,255,0.85); margin: 6px 0 0; font-size: 14px;">
                Novo feedback recebido no BlogGuide
            </p>
        </div>
        <div style="padding: 28px 30px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 10px 0; color: #888; font-size: 13px; width: 140px; vertical-align: top;">Título</td>
                    <td style="padding: 10px 0; color: #222; font-size: 15px; font-weight: 600;">{titulo}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; color: #888; font-size: 13px; vertical-align: top;">Usuário</td>
                    <td style="padding: 10px 0; color: #222; font-size: 14px;">{user_label}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; color: #888; font-size: 13px; vertical-align: top;">Canal de contato</td>
                    <td style="padding: 10px 0; color: #222; font-size: 14px;">{canal_label}</td>
                </tr>
                <tr>
                    <td style="padding: 10px 0; color: #888; font-size: 13px; vertical-align: top;">Contato</td>
                    <td style="padding: 10px 0; color: #222; font-size: 14px;">{contato_label}</td>
                </tr>
            </table>
            <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 18px 0;" />
            <h3 style="color: #333; font-size: 15px; margin: 0 0 10px;">Descrição</h3>
            <div style="background: #fff; border: 1px solid #e8e8e8; border-radius: 8px; padding: 16px; color: #333; font-size: 14px; line-height: 1.6; white-space: pre-wrap;">{descricao}</div>
        </div>
        <div style="background: #f0f0f0; padding: 14px 30px; text-align: center;">
            <p style="margin: 0; color: #999; font-size: 12px;">
                Enviado automaticamente pelo sistema BlogGuide
            </p>
        </div>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = f"BlogGuide <{SMTP_EMAIL}>"
    msg["To"] = FEEDBACK_RECIPIENT_EMAIL
    msg["Subject"] = subject

    # Versão texto simples (fallback)
    text_body = (
        f"Tipo: {tipo_label}\n"
        f"Título: {titulo}\n"
        f"Usuário: {user_label}\n"
        f"Canal de contato: {canal_label}\n"
        f"Contato: {contato_label}\n\n"
        f"Descrição:\n{descricao}"
    )
    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("E-mail de feedback enviado para %s", FEEDBACK_RECIPIENT_EMAIL)
        return True
    except Exception as exc:
        logger.error("Falha ao enviar e-mail de feedback: %s", exc)
        return False
