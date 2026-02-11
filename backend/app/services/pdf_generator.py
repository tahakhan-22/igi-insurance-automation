"""
PDF generator service
Converts HTML to PDF using WeasyPrint
"""
from io import BytesIO
from weasyprint import HTML, CSS


def html_to_pdf(html_content: str) -> bytes:
    """
    Convert HTML string to PDF bytes using WeasyPrint
    
    Args:
        html_content: HTML string to convert
        
    Returns:
        PDF file as bytes
    """
    # Create PDF from HTML
    pdf_file = BytesIO()
    
    # Custom CSS for better PDF output
    custom_css = CSS(string='''
        @page {
            size: A4;
            margin: 2cm;
        }
        body {
            font-family: Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 10px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f0f0f0;
            font-weight: bold;
        }
        h1 {
            color: #003366;
            font-size: 20pt;
        }
        h2 {
            color: #003366;
            font-size: 16pt;
            margin-top: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .section {
            margin-bottom: 20px;
        }
    ''')
    
    HTML(string=html_content).write_pdf(pdf_file, stylesheets=[custom_css])
    
    return pdf_file.getvalue()
