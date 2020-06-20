import logging
import os, sys
import requests
import azure.functions as func
from typing import *
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *



def main(myReq: func.HttpRequest):
    playbook_url = extract_url("https://www.politico.eu/newsletter/brussels-playbook/", ".front-list > li:nth-child(1) > article:nth-child(1) > div:nth-child(2) > article:nth-child(1) > div:nth-child(1) > header:nth-child(1) > h3:nth-child(1) > a:nth-child(1)", 'href')
    audio_url_brussels = extract_url(playbook_url, "#amazon-polly-audio-play > source:nth-child(1)", "src")

    for i in range(1, 3):
        playbook_url = extract_url("https://www.politico.eu/newsletter/london-playbook/", ".front-list > li:nth-child("+str(i)+") > article:nth-child(1) > div:nth-child(2) > article:nth-child(1) > div:nth-child(1) > header:nth-child(1) > h3:nth-child(1) > a:nth-child(1)", 'href')
        print(playbook_url)
        # check for "london playbook PM"
        if "-pm-" not in playbook_url:
            audio_url_uk = extract_url(playbook_url, "#amazon-polly-audio-play > source:nth-child(1)", "src")
            break
        else:
            pass

    send_us_playbook_url(audio_url_brussels, audio_url_uk)
    logging.info('Python HTTP triggered function processed ok!')

def extract_content(url) -> str:
    req = requests.get(url, headers = {"user-agent":"Azure Cloud @ GitHub"}).text
    return req

def extract_url(url, selector, attribute) -> str:
    soup = BeautifulSoup(extract_content(url), 'html.parser')
    tag = soup.select(selector)[0]
    url = tag.attrs[attribute]
    return url

def send_us_playbook_url(url_eu, url_uk) -> str:
    sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

    msg = '''Brussels: {0}
             London: {1}
            '''.format(url_eu, url_uk)

    message = Mail(from_email=From(os.environ.get('OUTLOOK_EMAIL'), 'My Outlook email'),
            to_emails=To(os.environ.get('SEZNAM_EMAIL'), 'My seznam email'),
            subject=Subject('Politico EU Podcast URL Direct Links'),
            plain_text_content=PlainTextContent(msg))
    try:
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
