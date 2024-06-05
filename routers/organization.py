from pydantic import validator
from utils import *
from imports import *
router = APIRouter()


@validator('skills', 'cause')
def check_max_items(cls, v):
        if len(v) > 3:
            raise ValueError('You can select a maximum of 3 items.')
        return v
# method for handling organization registration
@router.post("/register/organization")
async def register_organization(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    city: str = Form(...),
    priorities: str = Form(...),
    cause: str = Form(...),
    orgtype: str = Form(...),
    password: str = Form(...)
):

    form_data = {
        "name": name,
        "email": email,
        "city": city,
        "priorities": priorities,
        "cause": cause,
        "orgtype": orgtype,
        "password": password
    }

     # Hash the password
    password = hash_password(form_data['password'])
    # Call the register_user function
    register_user(request, organization_collection, "organization/register_organization.html", form_data, "/organization", "organization")

@router.post("/create-opportunity/")
async def create_opportunity(opportunity_data: Opportunity, request: Request):
    session_token = request.cookies.get('session_token')
    if not session_token:
        raise HTTPException(status_code=403, detail="Not logged in")

    session_data = sessions_collection.find_one({"_id": session_token})
    if not session_data or session_data.get("user_type") != "organization":
        raise HTTPException(status_code=403, detail="Unauthorized")

    opportunities_collection.insert_one(opportunity_data.dict())
    return JSONResponse(status_code=201, content={"message": "Opportunity created successfully"})

    #View opportunity listed
@router.get("/opportunities/")
async def view_opportunities(request: Request):
    session_token = request.cookies.get('session_token')
    if not session_token:
        return RedirectResponse(url="/login")
    user_data = sessions_collection.find_one({"_id": session_token})
    if not user_data or user_data['type'] != 'organization':
        return RedirectResponse(url="/login")
    opportunities = list(opportunities_collection.find({"organization_id": user_data['id']}))
    return templates.TemplateResponse("/volunteer/volunteer.html", {"request": request, "opportunities": opportunities})

@router.delete("/delete-opportunity/{opportunity_id}")
async def delete_opportunity(request: Request, opportunity_id: str):
    session_token = request.cookies.get('session_token')
    if not session_token:
        return JSONResponse(status_code=403, content={"message": "Not logged in"})

    user_data = sessions_collection.find_one({"_id": session_token})
    if not user_data or user_data['type'] != 'organization':
        return JSONResponse(status_code=403, content={"message": "Unauthorized"})

    # Delete the opportunity
    opportunities_collection.delete_one({"_id": ObjectId(opportunity_id), "organization_id": user_data['id']})
    return JSONResponse(status_code=200, content={"message": "Opportunity deleted successfully"})

