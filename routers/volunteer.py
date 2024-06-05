from utils import *
from imports import *


router = APIRouter()

# method for handling volunteer registration
@router.post("/register/volunteer")
async def register_volunteer(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    age: str = Form(...),
    gender: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    city: str = Form(...),
    skills: str = Form(...),
    cause: str = Form(...),
):
    # Extract form data
    form_data = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "gender": gender,
        "email": email,
        "password": password,
        "city": city,
        "skills": skills,
        "cause": cause
    }
    password = hash_password(form_data['password'])
    return register_user(request, volunteer_collection, "volunteer/register_volunteer.html", form_data, "/volunteer", "volunteer")
