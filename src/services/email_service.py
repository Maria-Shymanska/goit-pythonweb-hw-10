from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from aiosmtplib import send
from jinja2 import FileSystemLoader, Environment
from sqlalchemy import URL

from src.conf.config import config

from src.services.auth import create_email_token


async def send_email(email: str, username: str, host: URL):
    message = MIMEMultipart()
    message["From"] = config.MAIL_FROM
    message["To"] = email
    message["Subject"] = "Confirm email"

    token_verification = create_email_token({"sub": email})

    env = Environment(loader=FileSystemLoader(Path(__file__).parent / "templates"))
    template = env.get_template("verify_email.html")

    msg_content = template.render(
        username=username, host=host, token=token_verification
    )
    html_message = MIMEText(msg_content, "html")
    message.attach(html_message)

    try:
        await send(
            message,
            hostname=config.MAIL_SERVER,
            port=config.MAIL_PORT,
            use_tls=config.MAIL_SSL_TLS,
            username=config.MAIL_USERNAME,
            password=config.MAIL_PASSWORD,
            timeout=10.0,
        )
    except ConnectionError as err:
        print(str(err))