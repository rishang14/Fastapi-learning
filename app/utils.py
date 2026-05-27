from passlib.context import CryptContext  
import jwt 
from jwt.exceptions import InvalidTokenError 
from datetime import timedelta ,datetime,timezone



SECRET_KEY = "0c16b88ac2933ccb21bf374800a3b1abb56c55d3c3e6a06ba097024019dbb0d5" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")  




def create_token ( data:dict ,expires_delta: timedelta | None = None): 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_token


def decode_token(token): 
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except InvalidTokenError:
        return None