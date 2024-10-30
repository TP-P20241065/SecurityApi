import os
from fastapi_mail import ConnectionConfig, FastMail
from unit_management.controller.unit_controller import get_unit_by_id
from fastapi_mail import MessageSchema

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
        body="Hola " + str(first_name) + ", esta es su contraseña generada de su cuenta de ZuriCam:\n\n" + str(password),
        subtype="html"
    )
    return message


async def send_alert(address, incident, tracking_link, image, unit_id):
    unit = await get_unit_by_id(unit_id)
    car_plate = unit.result.carPlate
    email = os.getenv("AUTHORITIES_EMAIL")
    description = incident
    title = "ALERTA REPORTADA"

    if incident == '':
        email = os.getenv("SECURITY_EMAIL")
        description = "BOTÓN DE PÁNICO"
        title = description

    # Crear el mensaje
    message = MessageSchema(
        subject=str(title),
        recipients=[email],
        body="Incidencia: " + str(description) + "<br><br>"
             + "Dirección: " + str(address) + "<br><br>"
             + "Enlace de rastreo: " + str(tracking_link) + "<br><br>"
             + "Unidad: " + str(car_plate) + "<br><br>",
        subtype="html",
        attachments=[image]
    )

    return message
