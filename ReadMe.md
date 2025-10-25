Method	Endpoint	Description
GET	/send-verification	Sends verification code to Gmail

Request Example
GET http://*******/send-verification?gmail=example@gmail.com

RUN
uvicorn main:app --reload

.env file
GMAIL=*******
PASSWORD_GMAIL=*********
