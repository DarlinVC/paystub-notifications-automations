from fpdf import FPDF
import os

def generatePaystubPdf(data, country='es'):
    """
    :param data: a dict with keys:
        full_name (str)
        email (str)
        position (str)
        health_discount_amount (float)
        social_discount_amount (float)
        taxes_discount_amount (float)
        other_discount_amount (float)
        gross_salary (float)
        gross_payment (float)
        net_payment (float)
        period (str) e.g. '2025-03-10'
        company (str, optional): Company name for the logo.
    :param country: 'es' for Spanish (default) or 'en' for English
    """
    # Translations for Spanish and English
    translations = {
        'es': {
            'full_name': 'Nombre Completo',
            'email': 'Correo Electronico',
            'position': 'Cargo',
            'title': 'Comprobante de Pago',
            'gross_salary': 'Salario Bruto',
            'gross_payment': 'Pago Bruto',
            'net_payment': 'Pago Neto',
            'health_insurance': 'SFS',
            'social_security': 'AFP',
            'taxes': 'ISR',
            'others': 'Otros',
            'discounts': 'Descuentos',
            'total': 'Total',
            'employee_info': 'Información del Empleado',
            'salary_info': 'Información Salarial'
        },
        'en': {
            'full_name': 'Full Name',
            'email': 'Email',
            'position': 'Position',
            'title': 'Paystub',
            'gross_salary': 'Gross Salary',
            'gross_payment': 'Gross Payment',
            'net_payment': 'Net Payment',
            'health_insurance': 'Health Insurance',
            'social_security': 'Social Security',
            'taxes': 'Taxes',
            'others': 'Others',
            'discounts': 'Discounts',
            'total': 'Total',
            'employee_info': 'Employee Information',
            'salary_info': 'Salary Information'
        }
    }

    lang = translations.get(country, translations['es'])
    
    pdf = FPDF()
    pdf.add_page()

    # -- Header Section --
    company = data.get('company', None)
    assets_dir = os.path.join(os.path.dirname(__file__), '..', 'assets')
    if company:
        candidate_logo = os.path.join(assets_dir, f"{company}.png")
        if os.path.exists(candidate_logo):
            logo_path = candidate_logo
        else:
            logo_path = os.path.join(assets_dir, "default_logo.png")
    else:
        logo_path = os.path.join(assets_dir, "default_logo.png")
    
    pdf.image(logo_path, x=85, y=5, w=40)
    
    pdf.ln(35)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"{lang['title']} [{data['period']}]", ln=True, align='C')
    pdf.ln(5)
    
    # Employee Information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, lang['employee_info'], ln=True)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, f"{lang['full_name']}: {data['full_name']}", ln=True)
    pdf.cell(0, 8, f"{lang['email']}: {data.get('email', '')}", ln=True)
    pdf.cell(0, 8, f"{lang['position']}: {data['position']}", ln=True)
    pdf.ln(5)
    
    # Salary Information
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, lang['salary_info'], ln=True)
    
    pdf.set_font('Arial', '', 12)
    
    pdf.cell(60, 8, f"{lang['gross_salary']}:", border=1)
    pdf.cell(0, 8, f"{data['gross_salary']}", border=1, ln=True)
    
    pdf.cell(60, 8, f"{lang['gross_payment']}:", border=1)
    pdf.cell(0, 8, f"{data['gross_payment']}", border=1, ln=True)
    
    pdf.cell(60, 8, f"{lang['net_payment']}:", border=1)
    pdf.cell(0, 8, f"{data['net_payment']}", border=1, ln=True)
    pdf.ln(5)
    
    # Discounts
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, lang['discounts'], ln=True)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(60, 8, f"{lang['health_insurance']}:", border=1)
    pdf.cell(0, 8, f"{data['health_discount_amount']}", border=1, ln=True)
    
    pdf.cell(60, 8, f"{lang['social_security']}:", border=1)
    pdf.cell(0, 8, f"{data['social_discount_amount']}", border=1, ln=True)
    
    pdf.cell(60, 8, f"{lang['taxes']}:", border=1)
    pdf.cell(0, 8, f"{data['taxes_discount_amount']}", border=1, ln=True)
    
    pdf.cell(60, 8, f"{lang['others']}:", border=1)
    pdf.cell(0, 8, f"{data['other_discount_amount']}", border=1, ln=True)
    
    # Calculate and display total discounts
    total_discounts = (
        data['health_discount_amount'] +
        data['social_discount_amount'] +
        data['taxes_discount_amount'] +
        data['other_discount_amount']
    )
    pdf.ln(2)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(60, 8, f"{lang['total']} {lang['discounts']}:", border=1)
    pdf.cell(0, 8, f"{total_discounts}", border=1, ln=True)
    
    
    # Saving
    pdf_name = f"paystub_{data['full_name'].replace(' ', '_')}.pdf"
    assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets/pdfs')
    os.makedirs(assets_path, exist_ok=True)
    pdf_path = os.path.join(assets_path, pdf_name)
    pdf.output(pdf_path)
    
    return pdf_path
