import bcrypt
from jose import jwt
from datetime import datetime, timedelta

# --- 1. SETTINGS (Token settings) ---
SECRET_KEY = "09d58603e832d236b4d57c74c995d654f05a1e74" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- 2. HASHING LOGIC (Bcrypt 72-byte Fix) ---
def hash_password(password: str):
    # Password ko bytes mein badal kar 72 tak cut kiya taaki error na aaye
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # Match check karne ke liye logic (Direct Bcrypt)
    return bcrypt.checkpw(
        plain_password.encode('utf-8')[:72], 
        hashed_password.encode('utf-8')
    )

# --- 3. TOKEN LOGIC (Jo AttributeError de raha tha) ---
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Ye line JWT token generate karti hai
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt