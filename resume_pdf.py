from reportlab.lib.pagesizes import A4

from reportlab.pdfgen import canvas

from textwrap import wrap

def create_resume(employee, personal_info=None, education=None, skills=None, projects=None):

    file_name = "resume.pdf"

    pdf = canvas.Canvas(file_name, pagesize=A4)

    width, height = A4

    x = 40

    y = 800

    # Header

    pdf.setFont("Times-Bold", 22)

    pdf.drawCentredString(width / 2, y, "Curriculum Vitae")

    y -= 25

    # Employee Name

    pdf.setFont("Times-Bold", 16)

    pdf.drawCentredString(width / 2, y, employee.name)

    y -= 20

    pdf.line(x, y, width - x, y)

    y -= 25

    # Contact

    pdf.setFont("Helvetica-Bold", 14)

    pdf.drawString(x, y, "Contact")

    y -= 18

    pdf.setFont("Helvetica", 10)

    pdf.drawString(x + 5, y, f"Email: {employee.email}")

    y -= 14

    pdf.drawString(x + 5, y, f"Phone: {employee.phone}")

    y -= 25

    # Summary

    if employee.summary:

        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawString(x, y, "Summary")

        y -= 18

        pdf.setFont("Helvetica", 10)

        for line in wrap(employee.summary, 90):

            pdf.drawString(x + 5, y, line)

            y -= 14

        y -= 10

    # Personal Information

    if personal_info:

        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawString(x, y, "Personal Info")

        y -= 18

        pdf.setFont("Helvetica", 10)

        pdf.drawString(x + 5, y, f"DOB: {personal_info.dob}")

        y -= 14

        pdf.drawString(x + 5, y, f"Gender: {personal_info.gender}")

        y -= 14

        pdf.drawString(x + 5, y, f"Address: {personal_info.address}")

        y -= 25

    # Education

    if education:

        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawString(x, y, "Education")

        y -= 18

        pdf.setFont("Helvetica", 10)

        pdf.drawString(

            x + 5,

            y,

            f"{education.degree}, {education.institution} ({education.year_of_completion})"

        )

        y -= 25

    # Skills

    if skills:

        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawString(x, y, "Skills")

        y -= 18

        pdf.setFont("Helvetica", 10)

        skills_text = ", ".join(skill.skill_name for skill in skills)

        for line in wrap(skills_text, 90):

            pdf.drawString(x + 5, y, line)

            y -= 14

        y -= 10

    # Projects

    if projects:

        pdf.setFont("Helvetica-Bold", 14)

        pdf.drawString(x, y, "Projects")

        y -= 18

        for project in projects:

            if y < 80:

                pdf.showPage()

                y = 800

            pdf.setFont("Helvetica-Bold", 12)

            pdf.drawString(x + 5, y, project.project_name)

            y -= 14

            pdf.setFont("Helvetica", 10)

            pdf.drawString(x + 5, y, f"Role: {project.role}")

            y -= 14

            for line in wrap(project.description or "", 90):

                pdf.drawString(x + 5, y, line)

                y -= 14

            y -= 10

    pdf.save()

    return file_name
 
 