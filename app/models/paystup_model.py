from pydantic import BaseModel

class PaystubModel(BaseModel):
    country: str
    credentials: str
    company_name: str