import http.client
import ssl
from urllib.parse import urlparse

def tryhttps(url):
    url = urlparse(url)
    httpsconn = http.client.HTTPSConnection(url.path)
    try:
        httpsconn.request("HEAD", "/")
        return True
    except:
        return False

print(tryhttps('www.stealmylogin.com')) # unsecure site
print(tryhttps('www.google.com')) # secure site
