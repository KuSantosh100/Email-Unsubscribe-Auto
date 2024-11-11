from dotenv import load_dotenv
import os
import imaplib
from imaplib import IMAP4_SSL
import email

load_dotenv()

username = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

server = os.getenv('server') # server = "imap.gmail.com"
inbox = os.getenv('inbox')

def conn_to_email():
    conn = IMAP4_SSL(server)
    conn.login(username, password)
    conn.select("inbox")
    return conn

def search_for_email():
    conn = conn_to_email()
    _, data = conn.search(None, '(BODY "unsubscribed")')
    data = data[0].split()
    for num in data:
        _, data = conn.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    html_content = part.get_payload(decode=True).decode()
                    print(html_content)
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True).decode()
            
            if content_type == 'text/html':
                print(content)
    conn.logout()
                    
search_for_email()
