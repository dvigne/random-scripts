from imaplib import IMAP4_SSL
import getpass

client = IMAP4_SSL('imap-mail.outlook.com', 993)

client.login(str(input("Username: ")), getpass.getpass())

print(client.noop())
