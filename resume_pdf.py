from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap

def create_resume(employee):
    print("inside create_resume()")

    file_name = "resume.pdf"

    pdf = canvas.Canvas(file_name, pagesize=A4)

    width, height = A4

    x = 40

    y = 800

    pdf.setFont("Times-Bold", 20)

    pdf.drawCentredString(width/2, y, "Curriculum Vitae")

    y -= 20

    pdf.line(x, y, width - x, y) 

    y -= 30

    pdf.setFont("Helvetica-Bold", 16)

    pdf.drawString(x, y, employee.name)

    y -= 20

    pdf.setFont("Helvetica", 10)

    pdf.drawString(x + 5, y, employee.email)

    y -= 15

    pdf.drawString(x + 5, y, employee.phone)

    y -= 30

    pdf.save()
    
    import os
    print("PDF file created successfully.")
    print("Saved at:", os.path.abspath(file_name))


    return file_name
 