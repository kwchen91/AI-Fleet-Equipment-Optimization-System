# src/report_generator.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_report(kpi_data, sustain_data, circular_data):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("RPM Hire – Sustainability Report", styles['Title']))
    story.append(Spacer(1, 20))

    story.append(Paragraph("Key Performance Indicators:", styles['Heading2']))
    for k, v in kpi_data.items():
        story.append(Paragraph(f"{k}: {v}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Sustainability Metrics:", styles['Heading2']))
    for k, v in sustain_data.items():
        story.append(Paragraph(f"{k}: {v}", styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Circular Economy Recommendations:", styles['Heading2']))
    for item in circular_data:
        story.append(Paragraph(f"{item['equipment_id']} – {item['recommendation']} (Health {item['health_score']})", styles['Normal']))
    story.append(Spacer(1, 12))

    doc.build(story)
    buffer.seek(0)
    return buffer

