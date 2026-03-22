import os
import hashlib
import qrcode
from fpdf import FPDF

def generate_hash(email, course):
    return hashlib.sha256((email + course).encode()).hexdigest()

def generate_pdf(
    cert_id, name, email, course, cert_hash, filename,
    institution="Gayatri Vidya Parishad College Of Engineering For Women",
    signer="Authorized Signatory",
    logo_path=None
):
    # Ensure folder exists
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    # Generate QR code pointing to verification
    pc_ip = "10.44.107.135"  # your LAN IP, change if needed
    qr_data = f"http://{pc_ip}:5001/verify_form?cert_id={cert_id}&email={email}"
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_temp = "temp_qr.png"
    qr_img.save(qr_temp)

    # Create PDF
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()

    # Optional: add institution logo
    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, x=80, y=10, w=50)
        pdf.ln(30)
    else:
        pdf.ln(20)

    # Draw border
    pdf.set_line_width(1.5)
    pdf.rect(10, 10, 190, 277)

    # Title
    pdf.set_font("Arial", 'B', 28)
    pdf.set_text_color(76, 175, 80)  # Green
    pdf.cell(0, 20, "Certificate of Completion", ln=True, align="C")
    pdf.ln(5)

    # Recipient name
    pdf.set_font("Times", 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 12, name, ln=True, align="C")
    pdf.ln(5)

    # Course info
    pdf.set_font("Arial", '', 16)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 10, f"has successfully completed the course:", align="C")
    pdf.set_font("Arial", 'I', 20)
    pdf.set_text_color(0, 102, 204)  # Blue
    pdf.cell(0, 12, f"{course}", ln=True, align="C")
    pdf.ln(10)

    # Certificate ID and Hash
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Certificate ID: {cert_id}", ln=True, align="C")
    pdf.cell(0, 6, f"Certificate Hash: {cert_hash}", ln=True, align="C")
    pdf.ln(15)

    # Institution info
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Institution: {institution}", ln=True, align="C")
    pdf.ln(10)

    # Signature placeholder
    pdf.set_font("Arial", 'I', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, f"Digital Signature: {signer}", ln=True, align="C")

    # Add QR code
    pdf.image(qr_temp, x=80, y=200, w=50)

    # Save PDF
    pdf.output(filename)

    # Remove temporary QR code
    if os.path.exists(qr_temp):
        os.remove(qr_temp)