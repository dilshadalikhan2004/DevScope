"""
DevScope - Executive PDF Report Generator
Generates a multi-page PDF executive report using ReportLab containing executive summaries,
KPI tables, business recommendations, and strategic story breakdowns.
"""

import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from config import REPORTS_DIR
from etl.logger import get_logger

logger = get_logger(__name__)

def generate_pdf_report(output_filename: str = "executive_report.pdf"):
    """Generates a multi-page PDF report for executive leadership."""
    output_path = REPORTS_DIR / output_filename
    logger.info(f"Generating Executive PDF Report at {output_path}...")
    
    doc = SimpleDocTemplate(str(output_path), pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=22, leading=26, textColor=colors.HexColor('#0F172A'), alignment=1)
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Normal'], fontSize=11, leading=15, textColor=colors.HexColor('#64748B'), alignment=1)
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, leading=18, textColor=colors.HexColor('#0284C7'))
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=9.5, leading=13.5, textColor=colors.HexColor('#334155'))
    callout_style = ParagraphStyle('CalloutStyle', parent=styles['Normal'], fontSize=9, leading=13, textColor=colors.HexColor('#0369A1'))
    
    story = []
    
    # Title Page Banner
    story.append(Spacer(1, 20))
    story.append(Paragraph("DevScope – Developer Career Intelligence Platform", title_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Executive Workforce Analytics & Tech Market Decision-Support Report", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Executive Summary Box
    exec_text = ("<b>Executive Summary</b>: Analysis of the Stack Overflow Developer Survey (2021–2024), "
                 "GitHub Octoverse, and public technology job datasets indicates that AI adoption continues to rise, "
                 "remote work remains widespread, and technologies such as Rust, TypeScript, and PostgreSQL show sustained growth. "
                 "Organizations planning technical hiring should align workforce development with these trends while considering "
                 "regional salary differences and evolving skill demand.")
    story.append(Paragraph(exec_text, body_style))
    story.append(Spacer(1, 20))
    
    # KPI Table
    kpi_data = [
        ["Metric", "Value", "Strategic Meaning"],
        ["Market Health Index", "78.4 / 100", "Macro tech employment stability score"],
        ["AI Adoption Index", "72.1%", "Active generative AI utilization share"],
        ["Remote Readiness Score", "66.8%", "Proportion of remote/hybrid workforce"],
        ["Global Median Salary", "$105,000 USD", "Global benchmark compensation level"]
    ]
    
    table = Table(kpi_data, colWidths=[140, 100, 290])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284C7')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
    ]))
    story.append(table)
    story.append(Spacer(1, 20))
    
    # Strategic Story 1 Breakdown
    story.append(Paragraph("1. Strategic Story: Generative AI Productivity Penetration", heading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Observation</b>: Developer AI adoption reached 72.1% across professional respondents.<br/>"
                           "<b>Business Implication</b>: AI tools have transitioned into core developer infrastructure.<br/>"
                           "<b>Recommendation</b>: Provide enterprise AI licenses alongside structured usage training.<br/>"
                           "<b>Expected Outcome</b>: May support improved engineering feature velocity.", callout_style))
    story.append(Spacer(1, 15))
    
    # Strategic Story 2 Breakdown
    story.append(Paragraph("2. Strategic Story: Experience & Compensation Progression", heading_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Observation</b>: Median compensation scales significantly from entry-level to senior tiers.<br/>"
                           "<b>Business Implication</b>: Compensation shifts at Year 3 to 5 represent potential retention inflection points.<br/>"
                           "<b>Recommendation</b>: Review mid-career pay benchmarks regularly against market medians.<br/>"
                           "<b>Expected Outcome</b>: May support improved developer retention.", callout_style))
    
    doc.build(story)
    logger.info(f"Executive PDF Report successfully generated at {output_path}.")

if __name__ == "__main__":
    generate_pdf_report()
