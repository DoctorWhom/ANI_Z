#-*- coding: UTF-8 -*-
"""
+--------------------------------------------------------------------+
|            ___         ____    ___    ___                          |
|           /   \       |    \  |   |  |   |                         |
|          /  .  \      |     \ |   |  |   |   Seminar               |
|         /  /_\  \     |      \|   |  |   |                         |
|        /   ___   \    |   |\      |  |   |   Angewandte            |
|       /   /   \   \   |   | \     |  |   |   Neuroinformatik       |
|      /___/     \___\  |___|  \____|  |___|                         |
|                                                                    |
+--------------------------------------------------------------------+
| Copyright (c) 2015,                                                |
|     Neuroinformatics and Cognitive Robotics Labs                   |
|     at TU Ilmenau, Germany                                         |
|                                                                    |
| All rights reserved.                                               |
|                                                                    |
| Copying, resale, or redistribution, with or without modification,  |
| is strictly prohibited.                                            |
|                                                                    |
| THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBU-   |
| TORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT |
| NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FIT- |
| NESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL    |
| THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, IN-  |
| DIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES,  |
| EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                 |
+--------------------------------------------------------------------+

Content:
Functions for sending e-mails with TU Ilmenau account.

Implementation is based on example code from:
[1] https://docs.python.org/2/library/email-examples.html
[2] http://stackoverflow.com/questions/23171140/
           how-do-i-send-an-email-with-a-csv-attachment-using-python
[3] http://stackoverflow.com/questions/3362600/
           how-to-send-email-attachments-with-python

@author: Markus Eisenbach
@date:   2015/03/17
"""

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import string

from . import simple_gui

def send_mail(to, subject, text, files = None, from_ = "", user = "",
              password = ""):
    """
    sends an e-mail (with attachement) using tu-ilmenau mail server
    """
    msg = MIMEMultipart()
    msg["From"] = from_
    msg["To"] = to
    msg["Subject"] = subject

    body = MIMEText(text, 'plain')
    msg.attach(body)    
    
    for file_ in files or []:
        ctype, encoding = mimetypes.guess_type(file_)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        
        maintype, subtype = ctype.split("/", 1)
        
        if maintype == "text":
            fp = open(file_)
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(file_, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(file_, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(file_, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=file_)
        msg.attach(attachment)
    
    failed = False
    check_login = False
    # try to send email
    while True:
        if check_login:
            check_login = False
            if from_ == "":
                from_, user, password = simple_gui.mail_login()
            else:
                if user == "unknown":
                    from_, user, password = simple_gui.mail_login()
                else:
                    message = "Der Server verweigert den Zugang.\n" \
                                + "Bitte überprüfen Sie ihre Daten."
                    mark1 = string.find(from_, "\"")
                    mark2 = string.rfind(from_, "\"")
                    mark3 = string.find(from_, "<")
                    mark4 = string.rfind(from_, ">")
                    name = from_[mark1+1:mark2]
                    mailadress = from_[mark3+1:mark4]
                    fields = [name, mailadress, user, password]
                    from_, user, password = simple_gui.mail_login(message,
                                                                  fields)
            # check if cancel button was hit
            if user == "unknown":
                failed = True
                break
            
            # replace message
            msg.replace_header("From", from_)
            
        try:
            server = smtplib.SMTP()
            # TU Ilmenau: ausgehender Mail-Server (mit Authentifizierung):
            #     smail.tu-ilmenau.de, Port 25, Verbindungssicherheit STARTTLS
            # Quelle: http://www.tu-ilmenau.de/it-service/mitarbeiter/
            #                                  e-mail/konfigurationshinweise/
            server.connect("smail.tu-ilmenau.de", 25)
            server.starttls()
            server.login(user, password)
            server.sendmail(from_, to, msg.as_string())
            server.quit()
            break
        
        except smtplib.SMTPRecipientsRefused:
            # user data not correct
            # ask for data again
            check_login = True
            # start another while loop to try again
            
        except smtplib.SMTPAuthenticationError:
            # user/pw not correct
            # ask for data again
            password = "" # reset password field
            check_login = True
            # start another while loop to try again
            
        except:
            failed = True
            raise
        
    return not failed
    
def main():
    emailfrom, user, password = simple_gui.mail_login()
    emailto = emailfrom # send to yourself
    fileToSend = "send_mail.py"
    subject = "Test"
    text = "This test-mail was send by a python script (attached)."
    success = send_mail(emailto, subject, text, [fileToSend],
                        emailfrom, user, password)
    if success:
        print("Send e-mail was successfull.")
    else:
        print("Send e-mail failed.")

if __name__ == "__main__":
    main()
