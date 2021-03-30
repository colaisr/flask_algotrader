import os

from flask import render_template
from flask_mail import Message

from app import create_app
from app import mail


import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail





def send_email(recipient, subject, template, **kwargs):
    message = Mail(
        from_email='cola.isr@gmail.com',
        to_emails='cola.isr@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
    # app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    # with app.app_context():
    #     msg = Message(
    #         app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
    #         sender='cola.isr@gmail.com',
    #         recipients=[recipient])
    #     msg.body = render_template(template + '.txt', **kwargs)
    #     msg.html = render_template(template + '.html', **kwargs)
    #     mail.send(msg)

# def send_email(recipient, subject, template, **kwargs):
#     app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#     with app.app_context():
#         msg = Message(
#             app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
#             sender='cola.isr@gmail.com',
#             recipients=[recipient])
#         msg.body = render_template(template + '.txt', **kwargs)
#         msg.html = render_template(template + '.html', **kwargs)
#         mail.send(msg)
