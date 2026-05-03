import re
import os
from docx import Document
from docx.shared import Inches

def parse_markdown_to_docx(md_path, docx_path, image_paths):
    doc = Document()
    
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('---'):
            doc.add_page_break()
            continue
            
        if line.startswith('# '):
            doc.add_heading(line[2:].replace('**', ''), level=1)
            
            # Insert dashboard image after main title
            if "QA Assessment Report" in line and 'dashboard' in image_paths:
                doc.add_picture(image_paths['dashboard'], width=Inches(6.0))
                
        elif line.startswith('## '):
            doc.add_heading(line[3:].replace('**', ''), level=2)
            
            # Insert login image in Testing Approach
            if "Testing Approach" in line and 'login' in image_paths:
                doc.add_picture(image_paths['login'], width=Inches(6.0))
                
        elif line.startswith('### '):
            doc.add_heading(line[4:].replace('**', ''), level=3)
            
            # Insert invoice image before BUG-006
            if "BUG-006" in line and 'invoice' in image_paths:
                doc.add_picture(image_paths['invoice'], width=Inches(6.0))
                
        elif line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            _add_formatted_text(p, line[2:])
            
        elif re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s', '', line)
            p = doc.add_paragraph(style='List Number')
            _add_formatted_text(p, text)
            
        elif line.startswith('> '):
            p = doc.add_paragraph(style='Quote')
            _add_formatted_text(p, line[2:])
            
        elif line.startswith('|') and '---' not in line:
            # Handle basic tables later or as paragraph
            p = doc.add_paragraph()
            _add_formatted_text(p, line)
            
        elif line.startswith('`') and line.endswith('`') and len(line) > 2:
             p = doc.add_paragraph(line)
             
        else:
            p = doc.add_paragraph()
            _add_formatted_text(p, line)
            
    doc.save(docx_path)

def _add_formatted_text(paragraph, text):
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            paragraph.add_run(part)

image_paths = {
    'login': r'C:\Users\Admin\.gemini\antigravity\brain\90486898-1e0d-4539-8e3c-7a0baf4563d2\login_page_1777821512532.png',
    'dashboard': r'C:\Users\Admin\.gemini\antigravity\brain\90486898-1e0d-4539-8e3c-7a0baf4563d2\dashboard_page_1777821712420.png',
    'invoice': r'C:\Users\Admin\.gemini\antigravity\brain\90486898-1e0d-4539-8e3c-7a0baf4563d2\invoice_page_1777821804797.png'
}

md_path = r'd:\CodePlay\luminoflowinfo\problems.md'
docx_path = r'd:\CodePlay\luminoflowinfo\problems.docx'

parse_markdown_to_docx(md_path, docx_path, image_paths)
print("DOCX created successfully.")
