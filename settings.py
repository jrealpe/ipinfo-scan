import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


IPINFO_API_KEY = os.environ.get('IPINFO_API_KEY')
