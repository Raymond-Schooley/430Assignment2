import xmlrpc.client
import socket

# from https://stackoverflow.com/questions/4716598/safe-way-to-connect-to-rpc-server
# updated for python3

def tryrpc(url):
    a = xmlrpc.client.ServerProxy(url)

    try:
        a._()   # Call a fictive method.
    except xmlrpc.client.Fault:
        # connected to the server and the method doesn't exist which is expected.
        pass
    except socket.error:
        # Not connected ; socket error mean that the service is unreachable.
        return False

    # Just in case the method is registered in the XmlRPC server
    return True, a

print(tryrpc('http://dd:LNXFhcZnYshy5mKyOFfy@127.0.0.1:9001'))
