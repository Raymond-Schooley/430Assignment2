import subprocess
import os

def main():

    
    file = open('networkconfigoutput.txt', 'wb')
    
    #Ipconfig will get ipv4, ipv6 and subnet mask
    ipconfig_response = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE)
    for line in ipconfig_response.stdout:
        line = line.rstrip()
        print (line)
        file.write(line)
        file.write(b'\r\n')

    #Enter in ipv4 address to lookup fqdn
    ip = input('Enter an ip address to receive a fqnd ')
    fqdn_nslookup_response = subprocess.Popen(["nslookup", ip], stdout=subprocess.PIPE)
    for line in fqdn_nslookup_response.stdout:
        line = line.rstrip()
        print (line)
        file.write(line)
        file.write(b'\r\n')
        
    #Enter in a fully qualified domain name to find the ip address
    fqdn = input('Enter a fqdn ')
    ip_nslookup_result = subprocess.Popen(['nslookup', fqdn], stdout=subprocess.PIPE)
    for line in ip_nslookup_result.stdout:
        line = line.rstrip()
        print (line)
        file.write(line)
        file.write(b'\r\n')
        
    #ping uses icmp and will work with both ipv4 and ipv6
    ping_result = subprocess.Popen(['ping', ip], stdout=subprocess.PIPE)
    for line in ping_result.stdout:
        line = line.rstrip()
        print (line)
        file.write(line)
        file.write(b'\r\n')
        
    #tracert will also work with either ipv4 or ipv6, we can add a switch to force a version to be used
    tracert_result = subprocess.Popen(['tracert', ip], stdout=subprocess.PIPE)
    for line in tracert_result.stdout:
        line = line.rstrip()
        print (line)
        file.write(line)
        file.write(b'\r\n')

    file.close()
    os.startfile("networkconfigoutput.txt", "print")
main()
