
import ssl

from flask import render_template

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(recipient, subject, template, **kwargs):
    message = Mail(
        from_email='support@algotrader.company',
        to_emails=recipient,
        subject=subject,
        html_content=render_template(template + '.html', **kwargs))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        # ssl._create_default_https_context = ssl._create_unverified_context   #uncomment for debugging
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)


# def send_email_old(recipient, subject, template, **kwargs):
#     app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#     with app.app_context():
#         msg = Message(
#             app.config['EMAIL_SUBJECT_PREFIX'] + ' ' + subject,
#             sender='cola.isr@gmail.com',
#             recipients=[recipient])
#         msg.body = render_template(template + '.txt', **kwargs)
#         msg.html = render_template(template + '.html', **kwargs)
#         mail.send(msg)
