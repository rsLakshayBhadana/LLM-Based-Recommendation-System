import hashlib

# Simple in-memory "database"
users_db = {}

# Using hashing for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup window
def register_user(username, password):
    if username in users_db:
        return False  # username already occupied
    users_db[username] = hash_password(password)
    return True

# login window
def authenticate_user(username, password):
    if username not in users_db:
        return False  # User have to Signup first
    if users_db[username] == hash_password(password):
        return True  # Correct password
    return False  # Incorrect password
