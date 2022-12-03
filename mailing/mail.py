import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print(os.getcwd())

me = "hallo@lufobo.de"
my_password = r""
you = "hannes.brugger.007@gmail.com"

msg = MIMEMultipart()
msg['Subject'] = "Alert"
msg['From'] = me
msg['To'] = you

html = '<html><body><p>Hi, I have the following alerts for you!</p></body></html>'
text = MIMEText(html, 'html')
msg.attach(text)

# This example assumes the image is in the current directory
fp = open('qrcode001.png', 'rb')
msgImage = MIMEImage(fp.read())
fp.close()

# Define the image's ID as referenced above
msgImage.add_header('Content-ID', '<image1>')
msg.attach(msgImage)#<img src="cid:image1"><br><br>
msgText = MIMEText('<br><br><b>Some <i>HTML</i> text</b> and an image.Nifty!', 'html')
msg.attach(msgText)
