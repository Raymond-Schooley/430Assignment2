'''TCSS430 Assignment2
    Raymond Schooley
    Alec Bain
    Timothy Yang'''

import subprocess
import os

# program driver


def main():
    file = open('networkconfigoutput.txt', 'w')
    print("Running ipconfig to gather network information")
    get_network_info(file)

    get_ip_fqdn(file)

    file.close()

    userprint = input('Would you like to print these results to the default printer? Y for yes, anything else for no ')
    if userprint == "Y":
        os.startfile("networkconfigoutput.txt", "print")
    else:
        pass
    print('Network diagnostics complete!')
    exit


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
        ping(user, '-4', file)
        tracert(user, '-4', file)
    elif type == 2:
        print('You entered a ipv6 address, the fqdn is ' + get_fqdn(user))
        ping(user, '-6', file)
        tracert(user, '-6', file)
    else:
        ip = get_ip(user)
        ipv = what_is(ip)
        if ipv == 1:
            ipv = 4
        else:
            ipv = 6
        print('You entered a fully qualified domain name, the ipv' + str(ipv) + 'address is ' + ip)
        ping(ip, '-' + str(ipv), file)
        tracert(ip, '-' + str(ipv), file)


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
