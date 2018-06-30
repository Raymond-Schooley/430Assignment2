import subprocess

import os


import re

def main():



    
#file = open('networkconfigoutput.txt', 'wb')
    get_network_info()


    get_ip_fqdn()        



    #file.close()

    #os.startfile("networkconfigoutput.txt", "print")

def get_network_info():

    ipv4_id = 'IPv4 Address'
    ipv6_id = 'IPv6 Address'
    subnet_id = 'Sunet Mask '
    result = list()
    #Ipconfig will get ipv4, ipv6 and subnet mask

    ipconfig_response = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE)


    for line in ipconfig_response.stdout:

        line = line.decode('utf-8')
        line = line.strip()
        line = re.sub("[b']", '', line)
        str = line.split('.', 1)[0]
        #print(str, subnet_id)
        if str == ipv4_id or str == ipv6_id or str == subnet_id:
            str1 = line.split(':', 1)[1].strip()
            result.append(str1)
        #file.write(line)

        #file.write(b'\r\n')

    print(result)
    return result

def get_ip_fqdn():
    user = input('Enter a ip address or fqdn')

    type = what_is(user)

    if type == 1:
        print('You entered a ipv4 address, the fqdn is ' + get_fqdn(user))
        ping(user, '-4')
        tracert(user, '-4')
    elif type == 2:
        print('You entered a ipv6 address, the fqdn is ' + get_fqdn(user))
        ping(user, '-6')
        tracert(user, '-6')
    else:
        ipv6 = get_ip(user)
        print('You entered a fully qualified domain name, the ipv6 address is ' + ipv6)
        ping(ipv6, '-6')
        tracert(ipv6, '-6')


def ping(ip, switch):
    #ping uses icmp and will work with both ipv4 and ipv6

    ping_result = subprocess.Popen(['ping', ip, switch], stdout=subprocess.PIPE)


    for line in ping_result.stdout:

        line = line.rstrip()

        print(line)

        #file.write(line)

        #file.write(b'\r\n')



def tracert(ip, switch):
    #tracert will also work with either ipv4 or ipv6, we can add a switch to force a version to be used

    tracert_result = subprocess.Popen(['tracert', switch, ip], stdout=subprocess.PIPE)


    for line in tracert_result.stdout:

        line = line.rstrip()

        print(line)

        #file.write(line)

        #file.write(b'\r\n')



def get_fqdn(ip):
    result = 'Fail'
    fqdn_nslookup_response = subprocess.Popen(["nslookup", ip], stdout=subprocess.PIPE)
    for line in fqdn_nslookup_response.stdout:
        line = line.decode('utf-8')
        line = line.strip()
        line = re.sub("[b']", '', line)
        #print (line)
        temp = line.split(':', 1)
        if temp[0].strip() == 'Name':
            result = temp[1].strip()
    #print(result)
    return result

def get_ip(fqdn):
    result = 'Fail'
    ip_nslookup_response = subprocess.Popen(["nslookup", fqdn], stdout=subprocess.PIPE)
    for line in ip_nslookup_response.stdout:
        line = line.decode('utf-8')
        line = line.strip()
        line = re.sub("[b']", '', line)
        #print (line)
        temp = line.split(':', 1)
        if temp[0].strip() == 'Addresses':
            result = temp[1].strip()
    #print(result)
    return result

#function returns 1 for ipv4, 2 for ipv6, and 3 for fqdn
def what_is(user):
    if ':' in user:
        result = 2
    elif any(c.isalpha() for c in user):
        result = 3
    else:
        result = 1
    return result


main()
