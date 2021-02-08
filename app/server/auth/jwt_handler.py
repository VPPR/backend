import time
from typing import Dict

import jwt
from decouple import config

def token_response(token: str, expiry : time):
    return {
        "access_token": token,
        "expiry": time.strftime("%m/%d/%Y, %H:%M:%S",time.localtime(expiry))

    }

JWT_SECRET = config('secret')

def signJWT(user_id: str) -> Dict[str, str]:
    # Set the expiry time.
    payload = {
        'user_id': user_id,
        'expires': time.time() + 2400
    }
    return token_response(jwt.encode(payload, JWT_SECRET, algorithm="HS256"),payload['expires'])

def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token.encode(), JWT_SECRET, algorithms=["HS256"])
        return decoded_token if decoded_token['expires'] >= time.time() else None
    except:
        return None