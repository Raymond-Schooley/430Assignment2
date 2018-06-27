import socket
import netifaces

google_ip = '2607:f8b0:400a:809::200e'

#this is import for retrieving the subnet mask
interface = '{46DE3F82-8FB5-469E-8D06-EC97A8378082}'

#get this computer's ipv4 and ipv6 address
ipv4 = socket.getaddrinfo(socket.gethostname(), 0)[3][4][0]
ipv6 = socket.getaddrinfo(socket.gethostname(), 0)[2][4][0]
print(ipv4)
print(ipv6)

#get the subnet mask
print("Mask: ", netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask'])

#given an ip address get the fqdn
google_fqdn = socket.getfqdn(socket.gethostbyaddr(google_ip)[2][0])
print(google_fqdn)

#given the fqdn, get the ip address
#I'm typing google.com here but the fqdn which will look different still works
google_ip1 = socket.gethostbyname('google.com')
print(google_ip1)
