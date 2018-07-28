import smtplib

def trysmtp(url):
    sender = "test@test.com"
    receivers = [url]
    message = ""

    try:
       smtpObj = smtplib.SMTP('localhost')
       smtpObj.sendmail(sender, receivers, message)
       return True
    except smtplib.SMTPException:
       return False

print(trysmtp('sldfk'))
print(trysmtp('email@email.com'))
