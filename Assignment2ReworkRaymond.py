import subprocess

def main():
    #Ipconfig will get ipv4, ipv6 and subnet mask
    ipconfig_response = subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE).stdout.read()
    print(ipconfig_response)

    #Enter in ipv4 address to lookup fqdn
    ip = input('Enter an ip address to receive a fqnd')
    fqdn_nslookup_response = subprocess.Popen(["nslookup", ip], stdout=subprocess.PIPE).stdout.read()
    print(fqdn_nslookup_response)

    #Enter in a fully qualified domain name to find the ip address
    fqdn = input('Enter a fqdn')
    ip_nslookup_result = subprocess.Popen(['nslookup', fqdn], stdout=subprocess.PIPE).stdout.read()
    print(ip_nslookup_result)

    #ping uses icmp and will work with both ipv4 and ipv6
    ping_result = subprocess.Popen(['ping', ip], stdout=subprocess.PIPE).stdout.read()
    print(ping_result)

    #tracert will also work with either ipv4 or ipv6, we can add a switch to force a version to be used
    tracert_result = subprocess.Popen(['tracert', ip], stdout=subprocess.PIPE).stdout.read()
    print(tracert_result)

main()