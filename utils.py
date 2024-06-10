from imports import *

# Authentication functions starts here 

 #Verify the password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify the provided plain password against the hashed password.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# Check if the password meets complexity requirements
def is_password_complex(password: str) -> bool:
    """
    Check if the password meets complexity requirements.
    """
    min_length = 8
    has_lowercase = re.search(r'[a-z]', password)
    has_uppercase = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_special = re.search(r'[!@#$%^&*()-_+=]', password)
    return (
        len(password) >= min_length and
        has_lowercase and
        has_uppercase and
        has_digit and
        has_special
    )


# Function to hash
def hash_password(password: str) -> str:
  """
  Hash the provided password using bcrypt.
  """
  password_bytes = password.encode('utf-8')
  salt = bcrypt.gensalt()
  hashed_password = bcrypt.hashpw(password_bytes, salt)
  return hashed_password.decode('utf-8')


# Function to generate a random token
def generate_token():
    return secrets.token_urlsafe(32)


# Create session token
def create_session_token(email: str) -> str:
    """
    Generate a session token for the authenticated user.
    """
    token = secrets.token_urlsafe(32)
    return token


# Store session token
def store_session_token(session_token: str, email: str, expiration_time: datetime, user_type: str):
    """
    Store the session token, its expiration time, and user type in the session store (MongoDB).
    """
    session_data = {
        "_id": session_token,
        "email": email,
        "expiration_time": expiration_time,
        "user_type": user_type  
    }
    sessions_collection.insert_one(session_data)



# Get session token
def get_session_token(request: Request, user_type: Optional[str] = None):
    if user_type == "volunteer":
        cookie_name = "session_token_volunteer"
    elif user_type == "organization":
        cookie_name = "session_token_organization"
    else:
        cookie_name = "session_token"
    return request.cookies.get(cookie_name)


# Get valid session token
def get_valid_session_token(session_token: str = Depends(get_session_token)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Not logged in")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data:
        raise HTTPException(status_code=401, detail="Invalid session token")
    expiration_time = session_data["expiration_time"].replace(tzinfo=timezone.utc)
    if expiration_time < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session token expired")
    return session_token


# Get unique userID in the database
def get_user_id(request: Request):
    """
    Extract user ID from request cookies or headers.
    You need to define the logic based on how you store the user ID in your application.
    """
    user_id = request.cookies.get('user_id')
    if user_id:
        return user_id
    else:
        user_id = request.headers.get('X-User-ID')
        if user_id:
            return user_id
        else:
            return None



# General function for email checking
def check_email_availability(email: str) -> bool:
    # Check if email exists in the volunteer_collection
    volunteer_result = volunteer_collection.find_one({"email": email})
    if volunteer_result:
        return False
    # Check if email exists in the organization_collection
    organization_result = organization_collection.find_one({"email": email})
    if organization_result:
        return False
    return True


# Check if the email is available in either volunteer or organization collections
def check_email_availability(email: str) -> bool:
    volunteer = volunteer_collection.find_one({"email": email})
    organization = organization_collection.find_one({"email": email})
    return volunteer is None and organization is None


# General user registration function with email, password complexity checking, hashing of password, and session token integration
def register_user(request: Request, collection: Collection, template: str, form_data: dict, redirect_url: str, user_type: str):
    # Check if the email already exists in the database collection
    user = collection.find_one({"email": form_data['email']})
    if user:
        # Email already exists
        return templates.TemplateResponse(
            template,
            {"request": request, "error_message": "Email already exists. Login instead?"}
        )
    # Check if password meets complexity requirements
    if not is_password_complex(form_data['password']):
        # Password is not complex enough
        return templates.TemplateResponse(
            template,
            {"request": request, "error_message": "Password does not meet complexity requirements"}
        )
    # If email is unique and password is complex, proceed with registration
    # Hash the password
    password = hash_password(form_data['password'])
    # Store the hashed password in your database along with other user details
    user_data = {**form_data, "hashed_password": password, "user_type": user_type}
    del user_data['password']  # Remove plaintext password from user_data before storing
    collection.insert_one(user_data)
    # Generate a session token
    session_token = create_session_token(form_data['email'])
    # Set the expiration time for the session token (e.g., 1 hour from now)
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1)  # Ensure expiration time is in UTC
    # Store the session token, its expiration time, and user type in the session store
    if user_type == "volunteer":
        store_session_token(session_token, form_data['email'], expiration_time, user_type, form_data.get('name'))
    else:
        store_session_token(session_token, form_data['email'], expiration_time, user_type)
    # Determine the redirect URL based on the user's role
    redirect_url = "/volunteer" if user_type == "volunteer" else "/organization"
    # Create a RedirectResponse and set the session token cookie
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie("session_token", session_token, expires=expiration_time, secure=True, httponly=True)
    return response


# Reset password functions 
# Check if the email is available in either volunteer or organization collections
def check_email_availability(email: str) -> bool:
    volunteer = volunteer_collection.find_one({"email": email})
    organization = organization_collection.find_one({"email": email})
    return volunteer is None and organization is None


# Store the reset token in the database for the password reset
def store_reset_token(email, token):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    token_data = {
        "email": email,
        "token": token,
        "expires_at": expiration_time
    }
    tokens_collection.insert_one(token_data)

# Send password reset email
def send_email(email: str, link: str, subject: str):
    msg = MIMEMultipart()
    msg['From'] = 'do-not-reply@voluntech.com'
    msg['To'] = email
    msg['Subject'] = subject
    body = f'Click the following link to {subject}: {link}'
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.mailtrap.io', 587) as smtp:
        smtp.starttls()
        smtp.login('username', 'password')
        smtp.send_message(msg)

# Verify and update the user's password
def verify_and_update_password(email: str, new_password: str, token: str):
    # Check if the token is valid and not expired
    token_data = tokens_collection.find_one({"email": email, "token": token})
    if not token_data or datetime.utcnow() > token_data['expires_at']:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    # Hash the new password
    hashed_password = pwd_context.hash(new_password)
    # Update the password in the appropriate collection
    volunteer = volunteer_collection.find_one({"email": email})
    organization = organization_collection.find_one({"email": email})
    if volunteer:
        volunteer_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
    elif organization:
        organization_collection.update_one({"email": email}, {"$set": {"hashed_password": hashed_password}})
    else:
        raise HTTPException(status_code=400, detail="Email not found in any collection")
    # Clear the reset token after successful password update
    tokens_collection.delete_one({"email": email, "token": token})
    return {"message": "Password updated successfully"}

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

