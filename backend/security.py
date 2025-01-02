from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# Replace this with something more secure in real usage
# e.g., an environment variable, or store it hashed somewhere
SINGLE_PASSWORD = "asd"


def verify_password(credentials: HTTPBasicCredentials = Depends(security)):
    """
    A dependency that checks the supplied password via HTTP Basic Auth.
    If it doesn't match our SINGLE_PASSWORD, raise 401.
    """
    if credentials.password != SINGLE_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True
