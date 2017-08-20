import requests
import logging
import json
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

class SaltyClient():

    _LOGIN_URL = 'http://saltybet.com/authenticate?signin=1'

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.login()
    
    def login(self):
        payload = {
            'email' : self.email,
            'pword' : self.password,
            'authenticate' : 'signin'
        }
        session = requests.Session()
        session.post(self._LOGIN_URL, data=payload)
        self.session = session
        logging.info('Logged in as {0}'.format(self.email))

    def get_wallet_balance(self):
        ajax_response = self.session.get('http://saltybet.com/ajax_tournament_end.php')
        page_response = self.session.get('http://saltybet.com')
        clean_html = page_response.text.strip().strip('<!DOCTYPE html">')

        soup = BeautifulSoup(clean_html, 'html.parser')
        page_balance = soup.find_all(id='b')[0]['value']

        return {'ajax': response.text, 'page': page_balance}

    def get_tournament_balance(self):
        response = self.session.get('http://saltybet.com/ajax_tournament_start.php')
        return response.text

    def get_state(self):
        response = self.session.get('http://saltybet.com/state.json')
        state = json.loads(response.text)
        return state
