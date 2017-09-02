from config import config_default
from threading import Thread
from flask import render_template
from flask_mail import Mail, Message


def send_async_email(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(mail, to, subject, template, **kwargs):
    message = Message(config_default.FLASKY_MAIL_SUBJECT_PREFIX + subject,
                      sender=config_default.FLASKY_MAIL_SENDER,
                      recipients=to)
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    print(message)
    thr = Thread(target=send_async_email, args=[app, mail, message])
    thr.start()
    return thr