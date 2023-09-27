from fastapi import HTTPException, status

UserDoesNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Could not find user",
)
