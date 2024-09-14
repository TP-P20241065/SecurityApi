import os
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL"),
    MAIL_PASSWORD=os.getenv("PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


async def send_mms(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)


def send_email(email, first_name, password):
    message = MessageSchema(
        subject="Nueva contraseña",
        recipients=[email],
        body="Hola " + str(first_name) + ", esta es su contraseña generada de su cuenta de ZuriCam:\n\n" + str(
            password),
        subtype="html"
    )
    return message

def send_alert(address, incident, tracking_link, image, unit_id):
    email = os.getenv("AUTHORITIES_EMAIL")
    if incident == 'Botón de pánico':
        email = os.getenv("SECURITY_EMAIL"),

    message = MessageSchema(
        subject="Botón de pánico",
        recipients=[email],
        body="Incidencia: " + str(incident) + "\r\r\n"
        + "Dirección: " + str(address) + "\r\r\n"
        + "Imagen de rastreo: " + str(tracking_link) + "\r\r\n"
        + "Unidad: " + str(unit_id) + "\r\r\n"
        + "Imagen:\r\r\n" + str(image),
        subtype="html"
    )
    return message