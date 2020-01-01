import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

WAKUWAKU_LOGIN_USER = os.environ.get("WAKUWAKU_LOGIN_USER")
WAKUWAKU_LOGIN_PASSWORD = os.environ.get("WAKUWAKU_LOGIN_PASSWORD")
HAPPYMAIL_LOGIN_USER = os.environ.get("HAPPYMAIL_LOGIN_USER")
HAPPYMAIL_LOGIN_PASSWORD = os.environ.get("HAPPYMAIL_LOGIN_PASSWORD")
PCMAX_LOGIN_USER = os.environ.get("PCMAX_LOGIN_USER")
PCMAX_LOGIN_PASSWORD = os.environ.get("PCMAX_LOGIN_PASSWORD")
IKUKURU_LOGIN_USER = os.environ.get("IKUKURU_LOGIN_USER")
IKUKURU_LOGIN_PASSWORD = os.environ.get("IKUKURKU_LOGIN_PASSWORD")
