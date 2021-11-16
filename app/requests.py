import urllib.request
import json
from .models import Quotes



# function to get quote from API
def get_quote():
    response = requests.get('http://quotes.stormconsultancy.co.uk/random.json')
    if response.status_code == 200:
        quote = response.json()
        print(quote)
        return quote


        # http://quotes.stormconsultancy.co.uk/random.json