from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template
import os


import smtplib


def send_email(recipient, subject, template, **kwargs):
    gmail_user = os.environ.get('EMAIL_HOST_USER')
    gmail_password = os.environ.get('EMAIL_HOST_PASSWORD')
    me = gmail_user
    you = recipient
    TEXT_h = render_template(template + '.html', **kwargs)
    TEXT_t = render_template(template + '.txt', **kwargs)
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text =TEXT_t
    html = """\
    <html>
      <head></head>
      <body>
        {asparagus_cid}
      </body>
    </html>
    """.format(asparagus_cid=TEXT_h)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(me, you, msg.as_string())
        server.close()
        print('successfully sent the mail')
    except:
        print("failed to send mail")

# def send_email_works_plain(recipient, subject, template, **kwargs):
#     gmail_user = os.environ.get('EMAIL_HOST_USER')
#     gmail_password = os.environ.get('EMAIL_HOST_PASSWORD')
#     FROM = gmail_user
#     TO = recipient
#     SUBJECT = subject
#     TEXT = render_template(template + '.html', **kwargs)
#     full_html="""\
# <html>
#   <head></head>
#   <body>
# {asparagus_cid}
#   </body>
# </html>
# """.format(asparagus_cid=TEXT)
#
#     # Prepare actual message
#     message = """From: %s\nTo: %s\nSubject: %s\n\n%s
#     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
#
#     msg = "\r\n".join([
#         "From: user_me@gmail.com",
#         "To: user_you@gmail.com",
#         "Subject: Just a message",
#         "",
#         full_html
#     ])
#     try:
#         server = smtplib.SMTP("smtp.gmail.com", 587)
#         server.ehlo()
#         server.starttls()
#         server.login(gmail_user, gmail_password)
#         server.sendmail(FROM, TO, msg)
#         server.close()
#         print('successfully sent the mail')
#     except:
#         print("failed to send mail")

# def send_email_mailjet(recipient, subject, template, **kwargs):
#     api_key = os.environ.get('MAIL_JET_API_KEY')
#     api_secret = os.environ.get('MAIL_JET_API_SECRET')
#     print('keys')
#     print(api_key)
#     print(api_secret)
#     data = {
#         'Messages': [
#             {
#                 "From": {
#                     "Email": "support@stockscore.company",
#                     "Name": "Stock Score"
#                 },
#                 "To": [
#                     {
#                         "Email": recipient,
#                         "Name": "Dear"
#                     }
#                 ],
#                 "Subject": subject,
#                 "TextPart": "My first Mailjet email",
#                 "HTMLPart": render_template(template + '.html', **kwargs),
#                 "CustomID": "AppGettingStartedTest"
#             }
#         ]
#     }
#     try:
#
#         mailjet = Client(auth=(api_key, api_secret), version='v3.1')
#         result = mailjet.send.create(data=data)
#         print(result.status_code)
#         print(result.json())
#     except Exception as e:
#         print(e.message)

# def send_email_send_grid(recipient, subject, template, **kwargs):
#     message = Mail(
#         from_email='support@stockscore.company',
#         to_emails=recipient,
#         subject=subject,
#         html_content=render_template(template + '.html', **kwargs))
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         # ssl._create_default_https_context = ssl._create_unverified_context   #uncomment for debugging
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)
