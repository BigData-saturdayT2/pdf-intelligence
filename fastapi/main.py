from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, Field
import psycopg2
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from datetime import timedelta  # Import timedelta for setting expiration
from typing import Dict
import shutil

# FastAPI app instance
app = FastAPI()

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database connection parameters
DB_HOST = "104.196.119.128"
DB_PORT = "5432"
DATABASE = "postgres"
USER = "postgres-user"
PASSWORD = "zqA#q>pv`h3UG.XH"

# Get database connection
def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, 
        port=DB_PORT, 
        database=DATABASE, 
        user=USER, 
        password=PASSWORD
    )

# Pydantic models for user input
class User(BaseModel):
    username: str
    password: str

# Model for updating the password
class UpdatePasswordModel(BaseModel):
    old_password: str
    new_password: str

# Adjusted Settings model for JWT configuration
class Settings(BaseModel):
    authjwt_secret_key: str = Field(default="secret")
    authjwt_access_token_expires: int = 15  # Set token expiry in minutes

# Configuration for JWT Auth
@AuthJWT.load_config
def get_config():
    return Settings()

# Exception handler for authentication errors
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# Create user endpoint
@app.post("/signup")
def signup(user: User):
    hashed_password = pwd_context.hash(user.password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO assignment2.users (username, password) VALUES (%s, %s);", (user.username, hashed_password))
        conn.commit()
        return {"msg": "User created successfully"}
    except psycopg2.errors.UniqueViolation:
        return {"msg": "Username already exists"}
    finally:
        cursor.close()
        conn.close()

# Login endpoint with custom expiration time for access token
@app.post("/login")
def login(user: User, Authorize: AuthJWT = Depends()):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM assignment2.users WHERE username = %s;", (user.username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result or not pwd_context.verify(user.password, result[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Set access token to expire in 15 minutes
    expires_time = timedelta(minutes=15)  # Adjust the expiration time here as needed
    access_token = Authorize.create_access_token(subject=user.username, expires_time=expires_time)
    return {"access_token": access_token}

# Protected endpoint
@app.get("/protected")
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"message": f"Hello, {current_user}!"}

# View user profile
@app.get("/profile")
def view_profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    
    # Retrieve user details from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, created_at FROM assignment2.users WHERE username = %s;", (current_user,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if result:
        return {"username": result[0], "created_at": result[1]}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
# Define a dummy answer endpoint in FastAPI
@app.post("/answer-question")
def answer_question(data: Dict[str, str], Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    question = data.get("question", "")
    return {"answer": f"Received your question: {question}. This is a placeholder answer."}

@app.delete("/logout")
def logout(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Ensure user is logged in
    # Optionally add the token to a blacklist
    jti = Authorize.get_raw_jwt()["jti"]
    # ... blacklist logic ...
    return {"message": "Successfully logged out"}


# **Update Password Endpoint**
@app.put("/update-password")
def update_password(data: UpdatePasswordModel, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch current hashed password
    cursor.execute("SELECT password FROM assignment2.users WHERE username = %s;", (current_user,))
    result = cursor.fetchone()

    if not result or not pwd_context.verify(data.old_password, result[0]):
        raise HTTPException(status_code=401, detail="Old password is incorrect")

    # Update with the new password
    new_hashed_password = pwd_context.hash(data.new_password)
    cursor.execute("UPDATE assignment2.users SET password = %s WHERE username = %s;", (new_hashed_password, current_user))
    conn.commit()
    cursor.close()
    conn.close()

    return {"msg": "Password updated successfully"}
