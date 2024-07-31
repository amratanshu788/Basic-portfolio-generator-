import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as ReportLabImage
from reportlab.lib.units import inch
from io import BytesIO
import re

# Create the main application window
app = tk.Tk()
app.title("Portfolio Creator")
app.geometry("500x600")
app.resizable(False, False)

# Apple-like fonts and colors
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_LABEL = ("Helvetica", 12)
FONT_BUTTON = ("Helvetica", 12, "bold")
COLOR_BG = "#f2f2f2"

# Regular expression patterns for validation
PHONE_PATTERN = re.compile(r'^\d+$')
EMAIL_PATTERN = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')

# Create a function to handle the form submission


def submit_form():
    # Get the user input
    name = entry_name.get()
    number = entry_number.get()
    email = entry_email.get()
    qualification = entry_qualification.get()
    skills = entry_skills.get("1.0", tk.END).strip()

    # Validate the input
    if not name or not number or not email or not qualification or not skills:
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    if not PHONE_PATTERN.match(number):
        messagebox.showerror(
            "Error", "Please enter a valid mobile number (numbers only).")
        return

    if not EMAIL_PATTERN.match(email):
        messagebox.showerror("Error", "Please enter a valid email address.")
        return

    # Open file dialog to select a photo
    photo_filename = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if not photo_filename:
        messagebox.showerror("Error", "Please select a photo.")
        return

    # Open file dialog to save the PDF
    pdf_filename = filedialog.asksaveasfilename(
        defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_filename:
        messagebox.showerror(
            "Error", "Please choose a location to save the PDF.")
        return

    # Create the portfolio PDF
    try:
        generate_portfolio_pdf(pdf_filename, name, number,
                               email, qualification, skills, photo_filename)
        messagebox.showinfo(
            "Success", f"Portfolio created successfully.\nPDF saved as {pdf_filename}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create PDF: {e}")

# Function to generate the portfolio PDF


def generate_portfolio_pdf(filename, name, number, email, qualification, skills, photo_filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []

    # Set up styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = FONT_TITLE[0]
    title_style.fontSize = FONT_TITLE[1]
    title_style.alignment = 1

    label_style = styles['Normal']
    label_style.fontName = FONT_LABEL[0]
    label_style.fontSize = FONT_LABEL[1]

    skills_style = ParagraphStyle(
        name='SkillsStyle',
        parent=label_style,
        fontSize=FONT_LABEL[1] - 2,
        spaceAfter=12
    )

    # Add title
    story.append(Paragraph("Portfolio", title_style))

    # Add content
    story.append(Paragraph(f"Name: {name}", label_style))
    story.append(Paragraph(f"Number: {number}", label_style))
    story.append(Paragraph(f"Email: {email}", label_style))
    story.append(Paragraph(f"Qualification: {qualification}", label_style))
    story.append(Paragraph("Skills:", label_style))
    story.append(Paragraph(skills, skills_style))

    # Add the photo
    try:
        with Image.open(photo_filename) as photo:
            photo.thumbnail((200, 200))
            img_buffer = BytesIO()
            photo.save(img_buffer, format='JPEG')
            img_buffer.seek(0)
            img = ReportLabImage(img_buffer, width=2*inch, height=2*inch)
            story.append(img)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the image: {e}")

    # Build the PDF
    doc.build(story)


# Create the form labels
label_name = tk.Label(app, text="Name:", font=FONT_LABEL, bg=COLOR_BG)
label_name.pack(pady=(30, 5))
label_number = tk.Label(app, text="Number:", font=FONT_LABEL, bg=COLOR_BG)
label_number.pack()
label_email = tk.Label(app, text="Email:", font=FONT_LABEL, bg=COLOR_BG)
label_email.pack()
label_qualification = tk.Label(
    app, text="Qualification:", font=FONT_LABEL, bg=COLOR_BG)
label_qualification.pack()
label_skills = tk.Label(app, text="Skills:", font=FONT_LABEL, bg=COLOR_BG)
label_skills.pack()
label_photo = tk.Label(app, text="Upload Photo:", font=FONT_LABEL, bg=COLOR_BG)
label_photo.pack(pady=(30, 5))

# Create the form entry fields
entry_name = tk.Entry(app, font=FONT_LABEL)
entry_name.pack()
entry_number = tk.Entry(app, font=FONT_LABEL)
entry_number.pack()
entry_email = tk.Entry(app, font=FONT_LABEL)
entry_email.pack()
entry_qualification = tk.Entry(app, font=FONT_LABEL)
entry_qualification.pack()
entry_skills = tk.Text(app, width=40, height=5, font=FONT_LABEL)
entry_skills.pack()
button_upload = tk.Button(app, text="Browse...",
                          font=FONT_BUTTON, command=submit_form)
button_upload.pack(pady=(10, 30))

# Start the application
app.mainloop()
