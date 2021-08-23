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
