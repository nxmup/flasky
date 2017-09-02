from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    MAIL_SERVER='smtp.qq.com',
    MAIL_PORT='465',
    MAIL_USR_SSL=True,
    MAIL_USERNAME='2514980765',
    MAIL_PASSWORD='gpfldcqclxhcebih'
)
mail = Mail(app)


@app.route('/')
def index():
    msg = Message(subject='Hello, world', sender='Flasky Admin <2514980765@qq.com>',
                  recipients=['liuqi0315@gmail.com'])
    msg.html = "Test html"
    mail.send(msg)
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
