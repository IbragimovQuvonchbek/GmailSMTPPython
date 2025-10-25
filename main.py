from fastapi import FastAPI, HTTPException, Query
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from random import randint
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()


def send_email(receiver: str, code: int):
    sender_email = os.environ.get("GMAIL")
    sender_password = os.environ.get("PASSWORD_GMAIL")

    if not sender_email or not sender_password:
        raise Exception("GMAIL or PASSWORD_GMAIL is not set in environment variables")

    subject = "Lexicon.uz - Verification Code"
    body = f"Your Lexicon.uz verification code is: {code}"

    message = MIMEMultipart()
    message["From"] = formataddr(("Lexicon.uz", sender_email))
    message["To"] = receiver
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver, message.as_string())
    server.quit()


@app.get("/send-verification")
def send_verification(gmail: str = Query(...)):
    code = randint(100000, 999999)

    try:
        send_email(gmail, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "success": True,
        "message": "Verification email sent",
        "verification_code": code
    }
