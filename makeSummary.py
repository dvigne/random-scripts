from imaplib import IMAP4_SSL
import getpass
import time

client = IMAP4_SSL('imap-mail.outlook.com', 993)

try:
    client.login(str(raw_input("Username: ")), getpass.getpass())
except Exception:
    print("Login Failed")
    exit(1)

client.select('"System Events"', True)
print("Getting System Events Since %s" % time.strftime("%d-%b-%Y"))
type, messages = client.search(None, '(SUBJECT "System Event")', '(SINCE "%s")' % time.strftime("%d-%b-%Y"))
# type, messages = client.search(None, '(SUBJECT "System Event")')

messages = messages[0].split()

accounts = list()
alerts = list()

for message in messages:
    message = client.fetch(message, 'body[text]')

    body = str(message[1][0][1])

    values = body.replace('\\r\\n', '').splitlines()

    for x in range(0, len(values)):
        if("Account" == values[x].split(':')[0]):
            acct = values[x].split(':')[1].strip()
            alert = values[x + 3].split(':')[1].strip()
            if(accounts.count(acct) == 0):
                print("Found %s" % acct)
                accounts.append(acct)
                alerts.append([alert])
            else:
                if(alerts[accounts.index(acct)].count(alert) == 0):
                    alerts[accounts.index(acct)].append(alert)
print('\n')
print("-" * 5 + "Printable Output" + "-" * 5)
for account in range(0, len(accounts)):
    print("\n%s" % accounts[account])
    for alert in range(0, len(alerts[account])):
        print("\t - %s" % alerts[account][alert])

client.close()
client.logout()
