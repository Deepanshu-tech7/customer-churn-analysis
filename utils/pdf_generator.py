# utils/pdf_generator.py
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(customer_id, risk_prob, risk_level, recommendations, details):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#0f172a'), spaceAfter=15)
    section_title = ParagraphStyle('SecTitle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor('#635bff'), spaceAfter=12)
    body_style = ParagraphStyle('BodyTxt', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#334155'), leading=14)
    
    story.append(Paragraph("Enterprise Retainment Playbook", title_style))
    story.append(Spacer(1, 15))
    
    meta_table = [
        [Paragraph("<b>Target Customer:</b>", body_style), Paragraph(customer_id, body_style)],
        [Paragraph("<b>Attrition Probability:</b>", body_style), Paragraph(f"{risk_prob:.1%}", body_style)],
        [Paragraph("<b>Calculated Risk Level:</b>", body_style), Paragraph(risk_level, body_style)]
    ]
    t = Table(meta_table, colWidths=[150, 350])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    for rec in recommendations:
        story.append(Paragraph(f"<b>•</b> {rec}", body_style))
        story.append(Spacer(1, 6))
        
    doc.build(story)
    buffer.seek(0)
    return buffer
