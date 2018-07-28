from ftplib import FTP

def tryftp(url):
    ftp = FTP(url)
    try:
        ftp.connect()
        return True
    except:
        return False

print(tryftp('speedtest.tele2.net')) # public ftp
print(tryftp('google.com')) # not ftp
