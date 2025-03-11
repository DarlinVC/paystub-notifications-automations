import pandas as pd
import io
import os
import smtplib

from app.models import PaystubModel;
from app.services import generatePaystubPdf
from email.message import EmailMessage
from dotenv import load_dotenv


class PaystubService:
    def __init__(self, data):
        load_dotenv()
        self.country = data["country"]
        self.company_name = data["company_name"]
        self.payroll_data = data["payroll_data"]
        
        # email settings
        self.email_sender = os.getenv("EMAIL_SENDER")
        self.smtp_token = os.getenv("SMTP_TOKEN")
    
    async def processPayrollData(self):
        try:
            content = await self.payroll_data.read()
            decoded_content = content.decode("utf-8")
            df = pd.read_csv(io.StringIO(decoded_content))

            # Required cols
            required_columns = {
                "full_name", "email", "position", "health_discount_amount",
                "social_discount_amount", "taxes_discount_amount", "other_discount_amount",
                "gross_salary", "gross_payment", "net_payment", "period"
            }

            if not required_columns.issubset(df.columns):
                missing_columns = required_columns - set(df.columns)
                return {"error": f"Missing columns: {missing_columns}"}

            payroll_data = df.to_dict(orient="records")
            emails_sent = []
            
            for row in payroll_data:
                pdf_params = {
                    "full_name": row["full_name"],
                    "email": row["email"],
                    "position": row["position"],
                    "health_discount_amount": float(row["health_discount_amount"]),
                    "social_discount_amount": float(row["social_discount_amount"]),
                    "taxes_discount_amount": float(row["taxes_discount_amount"]),
                    "other_discount_amount": float(row["other_discount_amount"]),
                    "gross_salary": float(row["gross_salary"]),
                    "gross_payment": float(row["gross_payment"]),
                    "net_payment": float(row["net_payment"]),
                    "period": row["period"]
                }
                
                language = ""
                
                if self.country == "en":
                    language = "en"
                else:
                    language = "es"
                
                
                pdf_path = generatePaystubPdf(pdf_params, language);
                send_email = self.sendEmail(pdf_path, row["email"], row["period"])
                
                if send_email != False:
                    emails_sent.append(row["email"])
            
            return emails_sent            
        except Exception as e:
            print(e)
            return False;
    
    def sendEmail(self, pdf_path, email_receiver, period):
        # EMAIL SETTINGS (GMAIL IN THIS CASE)
        SMTP_SERVER = "smtp.gmail.com" 
        SMTP_PORT = 587 
        EMAIL_SENDER = self.email_sender
        # TOKEN
        EMAIL_TOKEN = self.smtp_token
        EMAIL_RECEIVER = email_receiver
          
        # CREATING MSG
        subject = ""
        if self.country == "en":
            subject = f"Paystub for period {period}"
        else:
            subject = f"Comprobante de sueldo para el perido: {period}"
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        
        with open(pdf_path, "rb") as pdf_file:
            pdf_data = pdf_file.read()
            msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))

        # SEND EMAIL
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  
                server.login(EMAIL_SENDER, EMAIL_TOKEN) 
                server.send_message(msg)  
            return email_receiver
        except Exception as e:
            print(e)
            return False
        