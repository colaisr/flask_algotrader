from flask import render_template
import os
from mailjet_rest import Client

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(recipient, subject, template, **kwargs):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "support@algotrader.company",
                    "Name": "Algotrader"
                },
                "To": [
                    {
                        "Email": recipient,
                        "Name": "Dear"
                    }
                ],
                "Subject": subject,
                "TextPart": "My first Mailjet email",
                "HTMLPart": render_template(template + '.html', **kwargs),
                "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    try:
        api_key = os.environ.get('MAIL_JET_API_KEY')
        api_secret = os.environ.get('MAIL_JET_API_SECRET')
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())
    except Exception as e:
        print(e.message)

def send_email_send_grid(recipient, subject, template, **kwargs):
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

