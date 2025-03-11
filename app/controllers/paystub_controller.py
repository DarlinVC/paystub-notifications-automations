import os
import secrets

from app.services import PaystubService
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv


router = APIRouter()
security = HTTPBasic()

load_dotenv()

# Store credentials in environment variables.
USERNAME = os.environ.get("API_USER", "default_user")
PASSWORD = os.environ.get("API_PWD", "default_pwd")

def get_current_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.post("/paystub_process/")
async def process_paystub(
    country: str = Form(...),
    credentials: str = Depends(get_current_credentials),
    company_name: str = Form(...),
    payroll_data: UploadFile = File(...)):
    # validations params
    required_fields = {"country": country, "payroll_data": payroll_data, "company_name": company_name}
    missing_fields = [field for field, value in required_fields.items() if not value]

    if missing_fields:
        raise HTTPException(status_code=422, detail="Missing required fields")
    
    # process
    params = {
        "country": country,
        "company_name": company_name,
        "payroll_data": payroll_data
    }
    
    _paystubService = PaystubService(params)
    results_paystub_process = await _paystubService.processPayrollData()
    
    if not results_paystub_process:
        raise HTTPException(status_code=500, detail="Process Failed")
    
    return {"emails_sent_successfully": results_paystub_process}
