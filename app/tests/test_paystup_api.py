import os
import pytest
from fastapi.testclient import TestClient
from app.main import app 
from app.services import PaystubService

class DummyPaystubService:
    def __init__(self, params):
        self.params = params
    
    async def processPayrollData(self):
        return [{"email": "john@example.com", "sent_at": "2025-03-11T00:00:00Z"}]

# Pytest's monkeypatch to override the PaystubService with our dummy.
@pytest.fixture(autouse=True)
def override_paystub_service(monkeypatch):
    monkeypatch.setattr("app.services.PaystubService", DummyPaystubService)

client = TestClient(app)

def test_process_paystub_success():
    # Sample CSV content
    csv_content = (
        "full_name,email,position,health_discount_amount,social_discount_amount,"
        "taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period\n"
        "John Doe,john@example.com,Developer,50,30,20,10,3000,2800,2700,2025-03-01\n"
    )
    
    response = client.post(
        "/paystub_process/",
        auth=("admin", "admin0102"),
        data={
            "country": "do",
            "company_name": "atdev"
        },
        files={
            "payroll_data": ("data.csv", csv_content, "text/csv")
        }
    )
    
    assert response.status_code == 200
    json_data = response.json()
    assert "emails_sent_successfully" in json_data
    assert isinstance(json_data["emails_sent_successfully"], list)
    # Verify the dummy response is returned.
    assert json_data["emails_sent_successfully"][0] == "john@example.com"

def test_process_paystub_missing_field():
    # Test the case when a required field (e.g., company_name) is missing.
    csv_content = (
        "full_name,email,position,health_discount_amount,social_discount_amount,"
        "taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period\n"
        "John Doe,john@example.com,Developer,50,30,20,10,3000,2800,2700,2025-03-01\n"
    )
    
    response = client.post(
        "/paystub_process/",
        auth=("admin", "admin0102"),
        data={
            "country": "do"
            # company_name is intentionally missing.
        },
        files={
            "payroll_data": ("data.csv", csv_content, "text/csv")
        }
    )
    
    # Expect a 400 error with a detail message indicating missing required fields.
    assert response.status_code == 422
    json_data = response.json()
    assert "company_name" in json_data["detail"][0]["loc"]
    assert json_data["detail"][0]["msg"] == "Field required"

def test_process_paystub_invalid_credentials():
    # Test using wrong credentials.
    csv_content = (
        "full_name,email,position,health_discount_amount,social_discount_amount,"
        "taxes_discount_amount,other_discount_amount,gross_salary,gross_payment,net_payment,period\n"
        "John Doe,john@example.com,Developer,50,30,20,10,3000,2800,2700,2025-03-01\n"
    )
    
    response = client.post(
        "/paystub_process/",
        auth=("wrong_user", "wrong_password"),
        data={
            "country": "do",
            "company_name": "atdev"
        },
        files={
            "payroll_data": ("data.csv", csv_content, "text/csv")
        }
    )
    
    # Expect a 401 Unauthorized error.
    assert response.status_code == 401
    json_data = response.json()
    assert json_data["detail"] == "Incorrect username or password"
