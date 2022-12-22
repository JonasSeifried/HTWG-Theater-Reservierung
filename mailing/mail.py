import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from QRCode import GenerateQR

def SendQR(dest_mail, url, information):

    GenerateQR(url)
    me = "hallo@lufobo.de"
    my_password = r"83v2pf7X9?uR"
    you = dest_mail

    msg = MIMEMultipart()
    msg['Subject'] = "Dein Code für das Theater"
    msg['From'] = me
    msg['To'] = you

    # This example assumes the image is in the current directory
    fp = open('qrcode001.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    with open("mail_qr.html", "r", encoding='utf-8') as f:
        html = f.read()
        html = html.replace('{%information%}', information)
        print(html)

    text = MIMEText(html, 'html')
    msg.attach(text)

    # Define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)        #<img src="cid:image1"><br><br>

    # Send the message via gmail's regular server, over SSL - passwords are being sent, afterall
    s = smtplib.SMTP_SSL('smtp.lufobo.de')
    # uncomment if interested in the actual smtp conversation
    # s.set_debuglevel(1)
    # do the smtp auth; sends ehlo if it hasn't been sent already

    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()

def SendVerify(dest_mail, url):

    me = "hallo@lufobo.de"
    my_password = r"83v2pf7X9?uR"
    you = dest_mail

    msg = MIMEMultipart()
    msg['Subject'] = "Bitte Bestätige deine Email"
    msg['From'] = me
    msg['To'] = you

    with open("mail_verify.html", "r", encoding='utf-8') as f:
        html = f.read()
        html = html.replace('{%url%}', url)
        print(html)

    text = MIMEText(html, 'html')
    msg.attach(text)

    s = smtplib.SMTP_SSL('smtp.lufobo.de')
    s.login(me, my_password)
    s.sendmail(me, you, msg.as_string())
    s.quit()