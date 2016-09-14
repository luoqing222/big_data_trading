"""This module define the messenger from the gmail account."""

__author__ = 'qingluo'

import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MessengerFromGmail(object):
    ''' class to send the messenge from the gmail account'''

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session

    def send_message(self, subject, body, to):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + to,
            "MIME-Version: 1.0",
            "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            to,
            headers + "\r\n\r\n" + body)

    def send_text_attachment(self, subject, to, text_file, folder):
        '''to send the email with attachment'''
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['To'] = to
        with open(folder + "/" +text_file, 'r') as fp:
            attachment = MIMEText(fp.read())
        
        attachment.add_header("Content-Disposition", "attachment", filename=text_file)
        msg.attach(attachment)

        self.session.sendmail(self.email, to, msg.as_string())

    def send_email(self, file_name, mail_list, folder):
        subject = file_name
        message = "This is a test message"
        for to in mail_list:
            self.send_text_attachment(subject, to, file_name, folder)

    def __del__(self):
        self.session.quit()
