from fastapi import FastAPI, HTTPException, Request, Form, Depends, APIRouter, Query
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic
from fastapi.staticfiles import StaticFiles
from datetime import datetime, timedelta, timezone
from pytz import utc
from typing import Dict, Optional, List
import bcrypt
import re
import secrets
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from pymongo.collection import Collection
from passlib.context import CryptContext
from models import volunteer, organization, ResetToken, Email, ResetPasswordData, Opportunity
from database import volunteer_collection, organization_collection, sessions_collection, tokens_collection, opportunities_collection
from routers.organization import router as organization_router
from routers.volunteer import router as volunteer_router
from routers.user_management import router as user_management
from bson import ObjectId
import logging


app = FastAPI()
security = HTTPBasic()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")