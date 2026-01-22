"""
Create a sample PDF for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_sample_pdf(filename="sample_resume.pdf"):
    """Create a sample resume PDF with sensitive information"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, height - 100, "John Doe")

    # Contact Information
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 130, "Email: john.doe@email.com")
    c.drawString(100, height - 150, "Phone: (555) 123-4567")
    c.drawString(100, height - 170, "LinkedIn: https://linkedin.com/in/johndoe")
    c.drawString(100, height - 190, "Portfolio: https://github.com/johndoe")

    # Work Experience
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 230, "Work Experience")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 260, "Senior Software Engineer at Tech Corp")
    c.drawString(100, height - 280, "Contact: +1-555-987-6543")

    # Education
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 320, "Education")

    c.setFont("Helvetica", 12)
    c.drawString(100, height - 350, "Bachelor of Science in Computer Science")
    c.drawString(100, height - 370, "Contact: alumni@university.edu")

    c.save()
    print(f"Created {filename}")

if __name__ == "__main__":
    create_sample_pdf()
