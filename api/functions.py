from django.conf import settings
import urllib.request
import urllib.parse
import json
import re
def verify_recaptcha(response):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': response
            }
    data = urllib.parse.urlencode(values).encode('utf-8')
    req = urllib.request.Request(url, data)
    response = urllib.request.urlopen(req)
    result = json.load(response)
    if result['success']:
        return True
    else:
        return False

    