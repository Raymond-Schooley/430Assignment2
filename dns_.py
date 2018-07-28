import http.client
import socket
import re

# from https://stackoverflow.com/a/1949507

def is_website_online(host):
    """ This function checks to see if a host name has a DNS entry by checking
        for socket info. If the website gets something in return,
        we know it's available to DNS.
    """
    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        return False
    else:
        return True


def is_page_available(host, path="/"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        False.
    """
    try:
        conn = http.client.HTTPConnection(host)
        conn.request("HEAD", path)
        if re.match("^[23]\d\d$", str(conn.getresponse().status)):
            return True
    except:
        return False

print(is_website_online('google.com'))
print(is_page_available('google.com'))

print(is_website_online('sdfsdfadklfjadfkkdf.com'))
print(is_page_available('sdfsdfadklfjadfkkdf.com'))
