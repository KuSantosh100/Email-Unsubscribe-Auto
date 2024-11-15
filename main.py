from dotenv import load_dotenv
import os
import imaplib
from imaplib import IMAP4_SSL
import email
from bs4 import BeautifulSoup # pip install beautifulsoup4
import requests # pip install requests

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


def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
    return links

def click_link(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print("Successfully visited", link)
        else:
            print("Failed to visit", link, "error code:", response.status_code)
    except Exception as e:
        print("Error with", link, str(e))
            

def search_for_email():
    conn = conn_to_email()
    _, data = conn.search(None, '(BODY "unsubscribed")')
    data = data[0].split()
    links = []
    
    for num in data:
        _, data = conn.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_payload(decode=True).decode()
                    links.extend(extract_links_from_html(html_content))
        else:
            content_type = msg.get_content_type()
            content = msg.get_payload(decode=True).decode()
            
            if content_type == 'text/html':
                links.extend(extract_links_from_html(content))
    conn.logout()
    return links
                    
links = search_for_email()
for link in links:
    click_link(link)