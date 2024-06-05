from utils import *
from imports import *

router = APIRouter()

# Login Function
@router.post("/login/")
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    # Check if email exists in either volunteer or organization collections
    volunteer = volunteer_collection.find_one({"email": email})
    organization = organization_collection.find_one({"email": email})
    if volunteer:
        user_type = "volunteer"
        user = volunteer
    elif organization:
        user_type = "organization"
        user = organization
    else:
        # Email not found in any collection, display alert
        return HTMLResponse(
            """
            <script>
                alert("Email not registered. Please sign up instead.");
                window.location.href = "/"; // Redirect to homepage or signup page
            </script>
            """
        )
    # Check if the password matches
    hashed_password = user.get("hashed_password")  # Retrieve hashed password from user
    if not hashed_password or not verify_password(password, hashed_password):
        # Password is incorrect, display alert
        return HTMLResponse(
            """
            <script>
                alert("Incorrect password");
                window.location.href = "/"; // Redirect to homepage or login page
            </script>
            """
        )
    # Generate a session token
    session_token = create_session_token(email)
    # Set the expiration time for the session token (e.g., 1 hour from now)
    expiration_time = datetime.now(timezone.utc) + timedelta(hours=1) 
    # Store the session token and its expiration time in the session store
    store_session_token(session_token, email, expiration_time, user_type)
    # Determine the redirect URL based on user type
    redirect_url = "/volunteer" if user_type == "volunteer" else "/organization"
    # Create RedirectResponse and set the session token cookie
    response = RedirectResponse(url=redirect_url, status_code=303)
    response.set_cookie("session_token", session_token, expires=expiration_time, secure=True, httponly=True)
    return response

# Logout using GET method
@router.get("/logout")
async def logout_get(session_token: str = Depends(get_session_token)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Not logged in")
    # Delete the session from the database
    result = sessions_collection.delete_one({"_id": session_token}) 
    if result.acknowledged and result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to logout")
    # Redirect to the home page after logout
    response = RedirectResponse(url="/")
    response.delete_cookie("session_token")  # Remove session token from client
    return response


# General method for checking email availability
@router.get("/check_email")
async def check_email(email: str):
    # Check if email exists in the volunteer_collection
    volunteer_result = volunteer_collection.find_one({"email": email})
    if volunteer_result:
        return {"available": False}
    # Check if email exists in the organization_collection
    organization_result = organization_collection.find_one({"email": email})
    if organization_result:
        return {"available": False}
    return {"available": True}




# Password reset with mailtrap integration for testing
@router.post("/send-password-reset-email/")
async def send_password_reset_email(email_data: Email):
    if not check_email_availability(email_data.email):
        token = generate_token()
        store_reset_token(email_data.email, token)
        reset_link = f"http://127.0.0.1:8000/reset-password?token={token}"
        send_email(email_data.email, reset_link, subject="Reset Your Password")
        return {"message": "Password reset email sent successfully"}
    else:
        raise HTTPException(status_code=400, detail="Email not found in database")

# Reset password based on unique user token sent from email
@router.post("/reset-password/")
async def reset_password(reset_data: ResetPasswordData):
    token_data = tokens_collection.find_one({"token": reset_data.token})
    if token_data and token_data["expires_at"] > datetime.utcnow():
        email = token_data["email"]
        verify_and_update_password(email, reset_data.new_password, reset_data.token)
        tokens_collection.delete_one({"token": reset_data.token})
        return {"message": "Password reset successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
