import PyPDF2
import docx
import os
import re
from email import message_from_bytes
from datetime import datetime

def process_document(filepath):
    """Extract text from various document formats"""
    if filepath.endswith('.pdf'):
        return extract_pdf_text(filepath)
    elif filepath.endswith('.docx'):
        return extract_docx_text(filepath)
    elif filepath.endswith('.eml'):
        return extract_email_text(filepath)
    else:
        raise ValueError("Unsupported file format")

def extract_pdf_text(filepath):
    """Extract text from PDF files"""
    text = ""
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return clean_text(text)

def extract_docx_text(filepath):
    """Extract text from DOCX files"""
    doc = docx.Document(filepath)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return clean_text(text)

def extract_email_text(filepath):
    """Extract text from EML files"""
    with open(filepath, 'rb') as file:
        msg = message_from_bytes(file.read())
    
    text_parts = []
    if msg.get('Subject'):
        text_parts.append(f"Subject: {msg['Subject']}")
    if msg.get('From'):
        text_parts.append(f"From: {msg['From']}")
    if msg.get('Date'):
        text_parts.append(f"Date: {msg['Date']}")
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                text_parts.append(part.get_payload(decode=True).decode())
    else:
        text_parts.append(msg.get_payload(decode=True).decode())
    
    return clean_text("\n".join(text_parts))

def clean_text(text):
    """Clean extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove headers/footers if needed
    return text.strip()
