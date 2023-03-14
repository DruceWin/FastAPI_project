from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt

from config import SECRET


class Auth:
    """Набор инструментов для аутентификации"""
    secret = SECRET

    def encode_access_token(self, email):
        """Метод для шифрования access токена"""
        payload = {
            'sub': email,
            'exp': datetime.utcnow() + timedelta(seconds=10),
            'scope': 'access_token',
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_access_token(self, token):
        """Метод для расшифровки access токена"""

        payload = jwt.decode(token, self.secret, algorithms=['HS256'])
        if payload['scope'] == 'access_token':
            return True
        #     raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        # except jwt.ExpiredSignatureError:
        #     raise HTTPException(status_code=401, detail='Token expired')
        # except jwt.JWTError:
        #     raise HTTPException(status_code=401, detail='Invalid token')
        return False


    def encode_refresh_token(self, email):
        """Метод для шифрования refresh токена"""
        payload = {
            'sub': email,
            'exp': datetime.utcnow() + timedelta(seconds=30),
            'scope': 'refresh_token',
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def get_new_refresh_or_401(self, refresh_token):
        """Метод возвращающий пару access и refresh"""
        try:
            payload = jwt.decode(token=refresh_token, key=self.secret, algorithms=['HS256'])
            if payload['scope'] == 'refresh_token':
                return {
                    'access_token': self.encode_access_token(payload['sub']),
                    'refresh_token': self.encode_refresh_token(payload['sub'])
                }
            raise HTTPException(status_code=401, detail='Invalid scope of token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail='Invalid token')
