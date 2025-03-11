from fpdf import FPDF
import os

def generatePaystubPdf(data, country='es'):
    """
    :param data:
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
    :param country: 'es' for Spanish (default), 'en' for English
    """
    # Translations for Spanish (es) and English (en)
    translations = {
        'es': {
            'title': 'Comprobante de pago',
            'gross_salary': 'Salario Bruto',
            'gross_payment': 'Pago Bruto',
            'net_payment': 'Pago Neto',
            'health_insurance': 'SFS',
            'social_security': 'AFP',
            'taxes': 'ISR',
            'others': 'Otros',
            'discounts': 'Descuentos',
            'total': 'Total'
        },
        'en': {
            'title': 'Paystub Payment',
            'gross_salary': 'Gross Salary',
            'gross_payment': 'Gross Payment',
            'net_payment': 'Net Payment',
            'health_insurance': 'Health Insurance',
            'social_security': 'Social Security',
            'taxes': 'Taxes',
            'others': 'Others',
            'discounts': 'Discounts',
            'total': 'Total'
        }
    }

    # Pick the correct language dictionary, default to Spanish if none found
    lang = translations.get(country, translations['es'])
    
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the title (Arial, Bold, 16 pt)
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'FakeClients', ln=True, align='C')
    pdf.ln(5)
    
    # Subtitle with the pay period
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"{lang['title']} [{data['period']}]", ln=True, align='C')
    pdf.ln(5)
    
    # Full name
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"{data['full_name']}", ln=True)
    
    # Position
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"{data['position']}", ln=True)
    pdf.ln(5)
    
    # Salary information
    pdf.cell(0, 10, f"{lang['gross_salary']}: {data['gross_salary']}", ln=True)
    pdf.cell(0, 10, f"{lang['gross_payment']}: {data['gross_payment']}", ln=True)
    pdf.cell(0, 10, f"{lang['net_payment']}: {data['net_payment']}", ln=True)
    pdf.ln(5)
    
    # Discounts
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"{lang['discounts']}", ln=True)
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"{lang['health_insurance']}: {data['health_discount_amount']}", ln=True)
    pdf.cell(0, 10, f"{lang['social_security']}: {data['social_discount_amount']}", ln=True)
    pdf.cell(0, 10, f"{lang['taxes']}: {data['taxes_discount_amount']}", ln=True)
    pdf.cell(0, 10, f"{lang['others']}: {data['other_discount_amount']}", ln=True)
    pdf.ln(5)
    
    # Calculate and display total discounts
    total_discounts = (
        data['health_discount_amount'] +
        data['social_discount_amount'] +
        data['taxes_discount_amount'] +
        data['other_discount_amount']
    )
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"{lang['total']}: {total_discounts}", ln=True)
    
    # Save PDF to a file named using the employee's name
    pdf_name = f"paystub_{data['full_name'].replace(' ', '_')}.pdf"
    assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets/pdfs')
    os.makedirs(assets_path, exist_ok=True)
    pdf_path = os.path.join(assets_path, pdf_name)
    pdf.output(pdf_path)
    
    return pdf_path