import datetime
import logging
import os, sys, json, io
import requests
import azure.functions as func
import lxml
from typing import *
from bs4 import BeautifulSoup


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    playbook_url = extract_main_playbook_url("https://www.politico.eu/newsletter/brussels-playbook/")


def extract_content(url) -> str:
    req = requests.get(url, headers = {"user-agent":"Azure Cloud @ GitHub"}).text
    return req

def extract_main_playbook_url(url) -> str:
    first_article_url_css_sel = ".front-list > li:nth-child(1) > article:nth-child(1) > div:nth-child(2) > article:nth-child(1) > div:nth-child(1) > header:nth-child(1) > h3:nth-child(1) > a:nth-child(1)"
    soup = BeautifulSoup(extract_content(url), 'html.parser')
    a_tag = soup.select(first_article_url_css_sel)[0]
    newest_playbook_issue_url = a_tag.attrs['href']
    return newest_playbook_issue_url

def extract_playbooks_polly_recording() -> str:






