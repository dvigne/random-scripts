from imaplib import IMAP4_SSL
import getpass
import time

client = IMAP4_SSL('imap-mail.outlook.com', 993)

client.login(str(input("Username: ")), getpass.getpass())

client.select('"System Events"', True)
type, messages = client.search(None, '(SUBJECT "System Event")', '(SINCE "%s")' % time.strftime("%d-%b-%Y"))

messages = messages[0].split()

alerts = set()

for message in messages:

    message = client.fetch(message, 'body[text]')

    body = str(message[1][0][1])

    values = body.split('\\r\\n')

    account = ''
    alert = ''
    for value in values:
        if("Account:" in value):
            alert += value.split(':')[1].strip()
        if("Subject:" in value):
            alert += value.split(':')[1].strip()

    alerts.append(alert)

print(alerts)

client.close()
client.logout()
