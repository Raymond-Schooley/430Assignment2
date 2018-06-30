import subprocess

import os


import re

#program driver
def main():



    
file = open('networkconfigoutput.txt', 'wb')
    get_network_info(file)


    get_ip_fqdn(file)        



    file.close()

    #os.startfile("networkconfigoutput.txt", "print")

'''runs the ipconfig command and parses it to find the useful info only
returns a list: result(ipv6, ipv4, subnet mask)'''

def get_network_info(file):
    #Header to identify our target info
    ipv4_id = 'IPv4 Address'
    ipv6_id = 'IPv6 Address'
    subnet_id = 'Sunet Mask '
    #list to return all info at once
    result = list()
    #Ipconfig will get ipv4, ipv6 and subnet mask

    ipconfig_response = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE)


    for line in ipconfig_response.stdout:

        #Apparently this returns something other than string so we need to convert to string
        line = line.decode('utf-8')
        line = line.strip()
        #get rid of weird characters
        line = re.sub("[b']", '', line)
        #break of the header part
        str = line.split('.', 1)[0]
        #check header
        if str == ipv4_id or str == ipv6_id or str == subnet_id:
            #When we find a target save to result list
            str1 = line.split(':', 1)[1].strip()
            result.append(str1)
        #file.write(line)

        #file.write(b'\r\n')

    print(result)
    return result


'''Get input from the user, call function to identify what type it is.
If it an ip address get the fqdn or vice versa
Finally call the ping and tracert commands with the info'''

def get_ip_fqdn(file):
    user = input('Enter a ip address or fqdn')

    #ipv4, ipv6, or fqdn?
    type = what_is(user)

    #Find corresponding info, call ping and tracert with appropriate option
    if type == 1:
        print('You entered a ipv4 address, the fqdn is ' + get_fqdn(user))
        ping(user, '-4', file)
        tracert(user, '-4', file)
    elif type == 2:
        print('You entered a ipv6 address, the fqdn is ' + get_fqdn(user))
        ping(user, '-6', file)
        tracert(user, '-6', file)
    else:
        ipv6 = get_ip(user)
        print('You entered a fully qualified domain name, the ipv6 address is ' + ipv6)
        ping(ipv6, '-6', file)
        tracert(ipv6, '-6', file)


'''We are just running ping and print results to a file'''

def ping(ip, option, file):
    ping_result = subprocess.Popen(['ping', ip, option], stdout=subprocess.PIPE)


    for line in ping_result.stdout:

        line = line.rstrip()

        print(line)

        #file.write(line)

        #file.write(b'\r\n')



'''We are just running tracert and print results to a file'''

def tracert(ip, option, file):
    tracert_result = subprocess.Popen(['tracert', option, ip], stdout=subprocess.PIPE)


    for line in tracert_result.stdout:

        line = line.rstrip()

        print(line)

        #file.write(line)

        #file.write(b'\r\n')




'''Given an ip address(ipv4 or ipv6) get the fqdn'''

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


'''Given a fqdn get the ipv6 address'''

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
