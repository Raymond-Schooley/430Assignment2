# TCSS430 Assignment6
#     Raymond Schooley
#     Alec Bain
#     Timothy Yang

import subprocess
import socket
import os
import smtplib
import ssl
import http.client
from urllib.parse import urlparse
from ftplib import FTP
import xmlrpc.client

# program driver.  Show user's network information.  Ask user to enter an ip address
#or a fully-qualified domain name before testing to see if various services are active on
#the romet host.
def main():
    #print everything to an output file
    file = open('networkconfigoutput.txt', 'w')
    print("Running ipconfig to gather network information")
    #Get info for local host
    get_network_info(file)

    #ask user for ip address or fqdn
    address = get_ip_fqdn(file)

    #test remote host to see which services are active
    get_smtp_status(file, address)
    get_rpc_status(file, address)
    get_http_status(file, address)
    get_ftp_status(file, address)
    get_ssh_status(file, address)
    get_ldap_status(file, address)
    get_dns_status(file, address)

    file.close()
    #Print results
    userprint = input('Would you like to print these results to the default printer? Y for yes, anything else for no ')
    if userprint == "Y":
        os.startfile("networkconfigoutput.txt", "print")
    else:
        pass
    print('Network diagnostics complete!')
    exit

#Tries to open an RPC connection
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_rpc_status(file, address):
    file.write('RPC Status:  ')
    print('RPC Status:  ')

    try:
        #establish connection
        proxy = xmlrpc.client.ServerProxy(str(address))
        #test connection
        proxy.system.listMethods()
        #print successful result
        file.write('Success')
        print('Success')
    #print failing result
    except OSError:
        file.write('Add http:// to domain name for RPC to work.')
        print('Add http:// to domain name for RPC to work.')
    except xmlrpc.client.Error:
        file.write('Partial Success (insufficient rights)')
        print('Partial Success (insufficient rights)')
    except ConnectionRefusedError:
        file.write('Refused')
        print('Refused')
    file.write('\r\n') 
            

#Tries to open an SMTP connection
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_smtp_status(file, address):
    file.write('SMTP Status:  ')
    print('SMTP Status:  ')
    try:
        # establish connection and test it
        smtplib.SMTP(str(address), 587)
        file.write('Success')
        # print successful result
        print('Success')
    except:
        # print failing result
        file.write('Failed (invalid address)')
        print('Failed (invalid address)')
    file.write('\r\n')

#Tries to connect via HTTP and HTTPS
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_http_status(file, address):
    file.write('HTTP Status:  ')
    print('HTTP Status:  ')
    url = urlparse(address)
    # establish connection
    httpconn = http.client.HTTPConnection(url.path)
    #test connection
    httpconn.request("HEAD", "/")
    httpresponse = httpconn.getresponse()
    if (httpresponse.status < 400):
        # print successful result
        file.write('Success')
        print('Success')
    else:
        # print failing result
        file.write('Failed')
        print('Failed')

    file.write('HTTPS Status:  ')
    print('HTTPS Status:  ')

    try:
        # establish connection
        httpsconn = http.client.HTTPSConnection(url.path)
        #test connection
        httpsconn.request("HEAD", "/")
        # print successful result
        file.write('Success')
        print('Success')
    except:
        # print failing result
        file.write('Failed')
        print('Failed')

#Tries to connect via FTP
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_ftp_status(file, address):
    file.write('FTP Status:  ')
    print('FTP Status:  ')
    try:
        # establish connection
        ftp = FTP(str(address))
        #test connection
        ftp.getwelcome()
        # print successful result
        file.write('Success')
        print('Success')
    except:
        # print failing result
        file.write('Failed')
        print('Failed')
    file.write('\r\n')

#Tries to connect to remote hosts well-known ssh port
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_ssh_status(file, address):
    file.write('SSH Status:  ')
    print('SSH Status:  ')

    #connect and test
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, 22))
    if result == 0:
        # print successful result
        print('Success')
    else:
        # print failing result
        print('Failed')

#Tries to connect to remote hosts well-known ldap port
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_ldap_status(file, address):
    file.write('LDAP Status:  ')
    print('LDAP Status:  ')

    # connect and test
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, 389))
    if result == 0:
        # print successful result
        print('Success')
    else:
        # print failing result
        print('Failed')

#Tries to connect to remote hosts well-known dns port
#param file - Output file to save all results
#param address - ip or fqdn of remote host
def get_dns_status(file, address):
    file.write('DNS Status:  ')
    print('DNS Status:  ')

    # connect and test
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, 53))
    if result == 0:
        # print successful result
        print('Success')
    else:
        # print failing result
        print('Failed')


'''runs the ipconfig command and parses it to find the useful info only
returns a list: result(ipv6, ipv4, subnet mask)'''
def get_network_info(file):
    # Header to identify our target info
    ipv4_id = 'IPv4 Address'
    ipv6_id = 'IPv6 Address'
    subnet_id = 'Subnet Mask'
  
    # list to return all info at once
    result = list()
    # Ipconfig will get ipv4, ipv6 and subnet mask

    ipconfig_response = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE)

    for line in ipconfig_response.stdout:

        # Apparently this returns something other than string so we need to convert to string
        line = line.decode('utf-8')
        line = line.strip()

        # break of the header part
        str = line.split('.', 1)[0].strip()
        # check header
        if str == ipv4_id or str == ipv6_id or str == subnet_id:

            # When we find a target save to result list
            str1 = line.strip()
            print(str1)
            #result.append(str1)
            #result.append('\n')
        file.write(line)

        file.write('\r\n')

    return result


'''Get input from the user, call function to identify what type it is.
If it an ip address get the fqdn or vice versa
Finally call the ping and tracert commands with the info'''


def get_ip_fqdn(file):
    user = input('Enter a ip address or fqdn to ping and traceroute ')

    # ipv4, ipv6, or fqdn?
    type = what_is(user)

    # Find corresponding info, call ping and tracert with appropriate option
    if type == 1:
        print('You entered a ipv4 address, the fqdn is ' + get_fqdn(user))
        # ping(user, '-4', file)
        # tracert(user, '-4', file)
    elif type == 2:
        print('You entered a ipv6 address, the fqdn is ' + get_fqdn(user))
        # ping(user, '-6', file)
        # tracert(user, '-6', file)
    else:
        ipv6 = get_ip(user)
        print('You entered a fully qualified domain name, the ipv6 address is ' + ipv6)
        # ping(ipv6, '-6', file)
        # tracert(ipv6, '-6', file)
    return user

'''We are just running ping and print results to a file'''


def ping(ip, option, file):
    ping_result = subprocess.Popen(
        ['ping', ip, option], stdout=subprocess.PIPE)

    for line in ping_result.stdout:

        # Apparently this returns something other than string so we need to convert to string
        line = line.decode('utf-8')
        line = line.strip()
        # get rid of weird characters
        print(line)

        file.write(line)

        file.write('\r\n')


'''We are just running tracert and print results to a file'''


def tracert(ip, option, file):
    tracert_result = subprocess.Popen(
        ['tracert', option, ip], stdout=subprocess.PIPE)

    for line in tracert_result.stdout:

        # Apparently this returns something other than string so we need to convert to string
        line = line.decode('utf-8')
        line = line.strip()
        # get rid of weird characters
        print(line)

        file.write(line)

        file.write('\r\n')


'''Given an ip address(ipv4 or ipv6) get the fqdn'''


def get_fqdn(ip):
    result = 'Fail'

    fqdn_nslookup_response = subprocess.Popen(
        ["nslookup", ip], stdout=subprocess.PIPE)

    for line in fqdn_nslookup_response.stdout:
        line = line.decode('utf-8')
        line = line.strip()
        #print (line)
        temp = line.split(':', 1)
        if temp[0].strip() == 'Name':
            result = temp[1].strip()
    # print(result)
    return result


'''Given a fqdn get the ipv6 address'''


def get_ip(fqdn):
    result = 'Fail'

    #Make sure to read the second address
    name = 'Name'
    right_address = False

    ip_nslookup_response = subprocess.Popen(
        ["nslookup", fqdn], stdout=subprocess.PIPE)
    for line in ip_nslookup_response.stdout:
        line = line.decode('utf-8')
        line = line.strip()
        print(line)
        temp = line.split(':', 1)

        header = temp[0].strip()

        if header == name:
            right_address = True
        if right_address and (header == 'Addresses' or header == 'Address'):
            result = temp[1].strip()
            print('Result is : ' + result)
    return result


'''function returns 1 for ipv4, 2 for ipv6, and 3 for fqdn'''


def what_is(user):
    if ':' in user:
        result = 2
    elif any(c.isalpha() for c in user):
        result = 3
    else:
        result = 1
    return result


main()
