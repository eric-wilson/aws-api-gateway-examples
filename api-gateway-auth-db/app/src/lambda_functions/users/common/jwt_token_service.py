import jwt
import uuid
import os
from datetime import timedelta, datetime

# todo ~ move these to secrets manager
SECRET_KEY=os.getenv("JWT_SECRET_KEY")
ISSUER_ID=os.getenv("JWT_ISSUER_ID")
AUDIENCE=os.getenv("JWT_AUDIENCE")
ALGORITHM=os.getenv("JWT_ALGORITHM")


if SECRET_KEY is None:
    SECRET_KEY="e044a525-9623-4a66-a641-9dcffa2aba75"

if ALGORITHM is None:
    ALGORITHM='HS256'


class RequestModel():
    def __init__(self) -> None:
        self.client_id = None
        self.expires_in_seconds = None
        self.email = None
        self.user = None    
        self.scopes = None


class TokenService():
    def __init__(self, secret=None, issuer=None, algorithm=None) -> None:
        
        if secret is None:
            secret = SECRET_KEY
        if issuer is None:
            issuer = ISSUER_ID
        if algorithm is None:
            algorithm = ALGORITHM
        self.secret = secret
        self.issuer = issuer
        self.algorithm = algorithm

    def encode_jwt_token(self, request: RequestModel=None):

        info = {
            "ref": str(uuid.uuid4()),
        }

        if request is not None:
            # removing audience for now ~ still working out how I want to map it
            # if request.client_id:
            #     info["aud"] = request.client_id
            if request.email:
                info["email"] = request.email
            if request.expires_in_seconds:
                info["exp"] = datetime.utcnow() + timedelta(seconds=request.expires_in_seconds)
            else:
                info["exp"] = datetime.utcnow() + timedelta(seconds=360)
            if request.scopes:
                info["scope"] = request.scopes
            if request.user:
                info["user"]= request.user


        token = jwt.encode(
            info,
            self.secret, algorithm=self.algorithm
        )
        return token
        

    def decode_jwt_token(self, encoded):
        decoded = jwt.decode(encoded, options={"verify_signature": False})
        return decoded

    def verify_jwt_token(self, encoded):

        encoded = str(encoded).removeprefix("Bearer").strip()

        decoded = jwt.decode(encoded, f'{self.secret}', algorithms=self.algorithm)

        #decoded = jwt.decode(encoded, f'{self.secret}', algorithms=self.algorithm, audience=AUDIENCE)

        return decoded

    def get_unverified_header(self, encoded):
        response = jwt.get_unverified_header(encoded)
        return response



