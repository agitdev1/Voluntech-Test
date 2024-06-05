from imports import *
from utils import *

#Organization router
app.include_router(organization_router)
#Volunteer router
app.include_router(volunteer_router)
#User management router
app.include_router(user_management)


#Landing Page
@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("/general/landing_page.html", {"request": request})


# ROUTES FOR DISPLAYING PAGES #

# Register Page
@app.get("/register", response_class=HTMLResponse)
async def get_signup_selection(request: Request):
    return templates.TemplateResponse("/general/register_selection.html", {"request": request})


# Route for displaying the volunteer page with logic to handle unauthorized access
@app.get("/volunteer", response_class=HTMLResponse)
async def get_volunteer_page(request: Request, session_token: str = Depends(get_session_token)):
    if not session_token:
        return RedirectResponse(url="/")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data:
        return RedirectResponse(url="/")
    expiration_time = session_data["expiration_time"].replace(tzinfo=utc)  # Make expiration_time timezone-aware
    if expiration_time < datetime.now(timezone.utc):
        return RedirectResponse(url="/")
    if session_data.get("user_type") != "volunteer":  # Check if the user type is not volunteer
        return RedirectResponse(url="/")  # Redirect to home if not volunteer
    
    # Fetch opportunities from the opportunities_collection
    opportunities = list(opportunities_collection.find({}))
    
    return templates.TemplateResponse("volunteer/volunteer.html", {"request": request, "opportunities": opportunities})


# Route for displaying the volunteer registration form
@app.get("/register/volunteer", response_class=HTMLResponse)
async def get_register_volunteer_form(request: Request):
    return templates.TemplateResponse("volunteer/register_volunteer.html", {"request": request})


# Route for displaying the organization page with logic to handle unauthorized acces
@app.get("/organization", response_class=HTMLResponse)
async def get_organization_page(request: Request, session_token: str = Depends(get_session_token)):
    if not session_token:
        return RedirectResponse(url="/")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data:
        return RedirectResponse(url="/")
    expiration_time = session_data["expiration_time"].replace(tzinfo=utc)  # Make expiration_time timezone-aware
    if expiration_time < datetime.now(timezone.utc):
        return RedirectResponse(url="/")
    if session_data.get("user_type") != "organization":  # Check if the user type is not organization
        return RedirectResponse(url="/")  # Redirect to home if not organization
    return templates.TemplateResponse("organization/organization.html", {"request": request})

# Route for displaying the orgnization registration form
@app.get("/register/organization", response_class=HTMLResponse)
async def get_register_organization_form(request: Request):
    return templates.TemplateResponse("organization/register_organization.html", {"request": request})

# Route for displaying the forogot password form
@app.get("/forgot-password", response_class=HTMLResponse)
async def get_forgot_password_form(request: Request):
    return templates.TemplateResponse("general/forgot_password.html", {"request": request})

# Route for displaying the forgot password form
@app.get("/reset-password", response_class=HTMLResponse)
async def get_reset_password_form(request: Request, token: str = Query(None), session_token: str = Depends(get_session_token)):
    if not token:
        return RedirectResponse(url="/forgot-password")
    return templates.TemplateResponse("general/reset_password.html", {"request": request})

# Create opportunity get method for organization
@app.get("/create-opportunity/", response_class=HTMLResponse)
async def create_opportunity_form(request: Request):
    session_token = request.cookies.get('session_token')
    if not session_token:
        return RedirectResponse(url="/")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data or session_data.get("user_type") != "organization":
        return RedirectResponse(url="/")
    return templates.TemplateResponse("/organization/create_opportunity.html", {"request": request})

#  Display profile page base on user type
@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request, session_token: str = Depends(get_session_token)):
    if not session_token:
        return RedirectResponse(url="/")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data:
        return RedirectResponse(url="/")
    expiration_time = session_data["expiration_time"].replace(tzinfo=utc)
    if expiration_time < datetime.now(timezone.utc):
        return RedirectResponse(url="/")
    user_type = session_data.get("user_type")
    if user_type == "volunteer":
        user_data = volunteer_collection.find_one({"email": session_data["email"]})
        return templates.TemplateResponse("volunteer/profile.html", {"request": request, "user_data": user_data})
    elif user_type == "organization":
        user_data = organization_collection.find_one({"email": session_data["email"]})
        return templates.TemplateResponse("organization/profile.html", {"request": request, "user_data": user_data})
    else:
        return RedirectResponse(url="/")

# Not fully implemented organization impact tracking
@app.get('/organization/impact', response_class=HTMLResponse)
def impact(request: Request):
    # Fetch data from database or service
    data = {
        'total_hours': 1500,
        'projects_completed': 75,
        'community_benefits': 'Improved local infrastructure and education'
    }
    return templates.TemplateResponse('organization/org_impact.html', {"request": request, **data})

# Not fully implemented volunteer impact tracking
@app.get('/volunteer/impact', response_class=HTMLResponse)
async def volunteer_impact(request: Request, session_token: str = Depends(get_session_token)):
    if not session_token:
        return RedirectResponse(url="/")
    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data:
        return RedirectResponse(url="/")
    expiration_time = session_data["expiration_time"].replace(tzinfo=utc)
    if expiration_time < datetime.now(timezone.utc):
        return RedirectResponse(url="/")
    if session_data.get("user_type") != "volunteer":
        return RedirectResponse(url="/")
    volunteer_data = volunteer_collection.find_one({"email": session_data["email"]})
    if not volunteer_data:
        return RedirectResponse(url="/")
    data = {
        'volunteer_name': volunteer_data.get('name', 'Volunteer'),
        'volunteer_hours': volunteer_data.get('hours', 0),
        'volunteer_projects_completed': volunteer_data.get('projects_completed', 0),
        'total_hours': 1500,  # Example static data
        'projects_completed': 75,  # Example static data
        'community_benefits': 'Various community benefits'  # Example static data
    }

    return templates.TemplateResponse('volunteer/volunteer_impact.html', {"request": request, **data})

