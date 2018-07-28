import pssh
from pssh.clients import ParallelSSHClient

# There has to be a better way.. Takes forever

def tryssh(url):
    try:
        client = ParallelSSHClient([url], user="FakeUserToTriggerException")
        client.run_command('ls')
    except pssh.exceptions.AuthenticationException:
        return True
    except pssh.exceptions.ConnectionErrorException:
        return False


print(tryssh('tty.sdf.org'))
print(tryssh('google.com'))
