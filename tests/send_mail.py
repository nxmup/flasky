from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["MAIL_SERVER"] = 'smtp.qq.com'
app.config["MAIL_PORT"] = 25
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "2514980765@qq.com"
app.config['MAIL_PASSWORD'] = 'wkpsqhkxzufudjfc'

mail = Mail(app)


@app.route('/')
def index():
    msg = Message(subject='Hello, world', sender='Flasky Admin <2514980765@qq.com>',
                  recipients=['liuqi0315@gmail.com'])
    msg.html = "Test html"
    print('Message is:', msg)
    mail.send(msg)
    return "<h1>OK!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
