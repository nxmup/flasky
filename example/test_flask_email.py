from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT='465',
    MAIL_USR_SSL=True,
    MAIL_USERNAME='2514980765',
    MAIL_PASSWORD='zfcxjvmnanmkdjab'
)
mail = Mail(app)


msg = Message(subject='Hello, world', sender='2514980765@qq.com',
              recipients=['liuqi0315@gmail.com'])
msg.html = "Test html"
with app.app_context():
    mail.send(msg)
