import logging
import os, sys, json, io
import requests
import azure.functions as func
from typing import *
from bs4 import BeautifulSoup
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

def main(myReq: func.HttpRequest):
    logging.info('Python HTTP triggered function processed:')
    playbook_url = extract_url("https://www.politico.eu/newsletter/brussels-playbook/", ".front-list > li:nth-child(1) > article:nth-child(1) > div:nth-child(2) > article:nth-child(1) > div:nth-child(1) > header:nth-child(1) > h3:nth-child(1) > a:nth-child(1)", 'href')
    audio_url = extract_url(playbook_url, "#amazon-polly-audio-play > source:nth-child(1)", "src")
    send_us_playbook_url(audio_url)

def extract_content(url) -> str:
    req = requests.get(url, headers = {"user-agent":"Azure Cloud @ GitHub"}).text
    return req

def extract_url(url, selector, attribute) -> str:
    soup = BeautifulSoup(extract_content(url), 'html.parser')
    tag = soup.select(selector)[0]
    url = tag.attrs[attribute]
    return url

def send_us_playbook_url(url) -> str:
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail(from_email=From(os.environ.get('OUTLOOK_EMAIL'), 'My Outlook email'),
                    to_emails=To(os.environ.get('SEZNAM_EMAIL'), 'My seznam email'),
                    subject=Subject('Politico Brussels Podcast URL Direct Link'),
                    plain_text_content=PlainTextContent('Brussels Playbook Podcast: ' + url))
# sendgrid key: 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

