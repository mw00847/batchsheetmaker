# original

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import math


def clean_table(table):
    return [[cell if cell and not (isinstance(cell, float) and math.isnan(cell)) else '' for cell in row] for row in table]

def clean_row(row):
    return [cell if cell and not (isinstance(cell, float) and math.isnan(cell)) else '' for cell in row]


def generate_pdf(data, headers, test_headers, test_data, matching_row, volume, weight, current_date):
    # Clean data to remove 'nan' values
    data = clean_table(data)
    test_data = clean_table(test_data)
    matching_row = clean_row(matching_row)

    filename = f"{matching_row[0]}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    elements = []

    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle('Custom', parent=styles['BodyText'], alignment=4, fontSize=9, leading=11)

    elements.append(
        Paragraph("batchsheetmaker", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=10, spaceAfter=6)))

    template1 = f"""
        {current_date}<br/><br/>
        PRODUCT: {matching_row[0]} LAB ITEM.: {matching_row[1]} REFERENCE: {matching_row[2]}<br/>
        VOLUME: {volume} WEIGHT: {weight}<br/><br/>
        VESSEL_________________ : D.O.M.______________ BATCH MAKER ________________<br/><br/>
    """
    elements.append(Paragraph(template1, custom_style))

    table = Table([headers] + data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    template3 = f"""
        METER READING_______ L BATCH WATER______L<br/>
        FINAL READING ______L CORRECTION _________L<br/>
        PART TO BE REBLENDED ________L<br/><br/>
        {matching_row[42]}<br/><br/>
        {matching_row[43]}<br/><br/>
    """

    elements.append(
        Paragraph("PROCEDURE/ HEALTH AND SAFETY", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=10, spaceAfter=6)))

    elements.append(Paragraph(template3, custom_style))

    elements.append(
        Paragraph("LAB TESTS", ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=10, spaceAfter=6)))

    test_table = Table([test_headers] + test_data, hAlign='LEFT')
    test_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(test_table)

    template4 = """
        Material passed as correct and ready for filling out<br/>
        SIGNED: _____________________________ DATE: ____________________
    """
    elements.append(Paragraph(template4, custom_style))

    doc.build(elements)
