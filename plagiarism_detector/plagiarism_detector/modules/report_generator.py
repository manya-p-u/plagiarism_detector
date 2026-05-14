from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(score, matches, path):
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>Plagiarism Report</b>", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"Similarity Score: {score}%", styles['Heading2']))
    content.append(Spacer(1, 20))

    content.append(Paragraph("<b>Copied Content:</b>", styles['Heading3']))
    content.append(Spacer(1, 10))

    for m in matches:
        content.append(Paragraph(m[0], styles['Normal']))
        content.append(Spacer(1, 10))

    doc.build(content)