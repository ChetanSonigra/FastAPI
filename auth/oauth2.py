from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime,timedelta, UTC
from typing import Optional
from jose import jwt, JWTError
import os
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.db_user import get_user_by_username

oauth2schema = OAuth2PasswordBearer(tokenUrl='token')


SECRET_KEY = str(os.environ.get("FASTAPI_SECRET_KEY"))
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(UTC) + expires_delta
  else:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def get_current_user(token: str = Depends(oauth2schema),db: Session = Depends(get_db)):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate":"Bearer"}
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception
  
  user = get_user_by_username(db,username)

  if user is None:
    raise credentials_exception
  return user