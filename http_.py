import http.client
from urllib.parse import urlparse

def tryhttp(url):
    url = urlparse(url)
    httpconn = http.client.HTTPConnection(url.path)
    httpconn.request("HEAD", "/")
    httpresponse = httpconn.getresponse()
    #print(httpresponse.status)
    if (httpresponse.status < 400):
        return True
    else:
        return False

print(tryhttp('www.stealmylogin.com')) # unsecure site
