from os import environ

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

if "PASSWORD" in environ:
    PASSWORD = environ["PASSWORD"]
else:
    raise Exception("PASSWORD environment variable not set")


def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """
    A dependency that checks the supplied password via HTTP Basic Auth.
    If it doesn't match our SINGLE_PASSWORD, raise 401.
    """
    if credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
