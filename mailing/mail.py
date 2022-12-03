import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

me = "hallo@lufobo.de"
my_password = r""
my_smtp = "smtp.lufobo.de"
you = "hannes.brugger.007@gmail.coe"
text = "Hallöle :)"


mail = MIMEText(text)
mail['Subject'] = "Testchen"
mail['From'] = "HTWG-Theater <hannes@lufobo.de>"
mail['To'] = "hannes.brugger.007@gmail.com"

sender = smtplib.SMTP(my_smtp, 587)

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
sender.ehlo()
sender.starttls(context=context)
sender.ehlo()

sender.login(me, my_password)
sender.send_message(mail)
sender.close()
