from app.services import PaystubService
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form

router = APIRouter()

@router.post("/paystub_process/")
async def process_paystub(
    country: str = Form(...),
    credentials: str = Form(...),
    company_name: str = Form(...),
    payroll_data: UploadFile = File(...)):
    # validations params
    required_fields = ["country", "credentials", "payroll_data", "company_name"]
    missing_fields = [field for field in required_fields if not locals().get(field)]

    if missing_fields:
        raise HTTPException(status_code=400, detail=f"Missing required fields: {', '.join(missing_fields)}")
    
    # process
    params = {
        "country": country,
        "credentials": credentials,
        "company_name": company_name,
        "payroll_data": payroll_data
    }
    
    _paystubService = PaystubService(params)
    results_paystub_process = await _paystubService.processPayrollData()
    
    if not results_paystub_process:
        raise HTTPException(status_code=500, detail="Process Failed")
    
    return {"results": results_paystub_process}
