import streamlit as st
import google.generativeai as genai
from PIL import Image as PILImage
import pytesseract
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import Image as ReportLabImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import os
import re

# Set up Google Gemini API
genai.configure(api_key="AIzaSyAiP-PYspe7CfXeJgeeEDtEuSkJCS-uBig")

# Email configuration (replace with your details)
EMAIL_ADDRESS = "gantihemanth143@gmail.com"
EMAIL_PASSWORD = "eqtj mltm wzxp uygs"  # Use App Password if using Gmail

# Function to extract text from an image using Tesseract OCR
def extract_text_from_image(image):
    image = image.convert('RGB')
    return pytesseract.image_to_string(image)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to clean and filter text
def clean_text(text):
    text = re.sub(r'\*+', '', text)
    text = re.sub(r'\n+', '\n', text).strip()
    return text

# Function to parse prescription analysis text into a table format
def parse_prescription_analysis_to_table(prescription_analysis_text):
    table_data = [["Medicine", "Dosage", "Frequency"]]  # Table header
    # Split by semicolon to separate different medicines, and exclude "Patient age" part
    medicines = [m.strip() for m in prescription_analysis_text.split(';') if not m.strip().startswith("Patient age")]
    for medicine_entry in medicines:
        if medicine_entry:
            try:
                # Expected format: "Medicine Dosage - Frequency"
                # Example: "Betaloc 100mg - 1 tab BID"
                parts = medicine_entry.split(' - ')
                if len(parts) == 2:
                    medicine_dosage = parts[0].strip()
                    frequency = parts[1].strip()
                    # Split medicine_dosage into medicine and dosage
                    medicine_parts = medicine_dosage.split(' ', 1)
                    if len(medicine_parts) == 2:
                        medicine = medicine_parts[0].strip()
                        dosage = medicine_parts[1].strip()
                        table_data.append([medicine, dosage, frequency])
                    else:
                        table_data.append([medicine_dosage, "", frequency])
                else:
                    table_data.append([medicine_entry.strip(), "", ""])
            except:
                table_data.append([medicine_entry.strip(), "", ""])
    return table_data

# Function to generate PDF report
def generate_pdf_report(prescription_text, user_problem, user_allergy, analysis_result, patient_name, patient_age, patient_sex):
    pdf_file = "report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter, topMargin=30, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom styles for headings, text, and footer
    styles.add(ParagraphStyle(name='MainHeading', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER, textColor=HexColor('#2ecc71')))
    styles.add(ParagraphStyle(name='SubHeading', fontName='Helvetica-Bold', fontSize=14, alignment=TA_LEFT, textColor=HexColor('#2ecc71')))
    styles.add(ParagraphStyle(name='NormalText', fontName='Helvetica', fontSize=12, alignment=TA_LEFT, leading=14))
    styles.add(ParagraphStyle(name='FooterText', fontName='Helvetica-Oblique', fontSize=10, alignment=TA_CENTER, textColor=HexColor('#FF0000')))
    styles.add(ParagraphStyle(name='PageNumber', fontName='Helvetica', fontSize=10, alignment=TA_CENTER))

    story = []

    # Logo (top-left)
    try:
        logo = ReportLabImage("logo.png", width=100, height=50)
        logo.hAlign = 'LEFT'
        story.append(logo)
    except:
        story.append(Paragraph("Logo Not Found", styles['NormalText']))
    story.append(Spacer(1, 12))

    # Main Heading (centered)
    story.append(Paragraph("Medical Report", styles['MainHeading']))
    story.append(Spacer(1, 24))

    # Patient Information Section
    story.append(Paragraph("Patient Information", styles['SubHeading']))
    story.append(Spacer(1, 6))
    story.append(Table([[""]], colWidths=[510], rowHeights=[10], style=[
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#2ecc71')),
    ]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Name: {patient_name if patient_name else 'Not Provided'}", styles['NormalText']))
    story.append(Paragraph(f"Age: {patient_age if patient_age else 'Not Provided'}", styles['NormalText']))
    story.append(Paragraph(f"Sex: {patient_sex if patient_sex else 'Not Provided'}", styles['NormalText']))
    story.append(Paragraph(f"Reported Symptoms: {clean_text(user_problem) if user_problem else 'Not provided'}", styles['NormalText']))
    story.append(Paragraph(f"Allergies: {clean_text(user_allergy) if user_allergy else 'No allergies'}", styles['NormalText']))
    story.append(Spacer(1, 24))

    # Prescription Analysis Section (using parsed Gemini API output)
    story.append(Paragraph("Prescription Analysis", styles['SubHeading']))
    story.append(Spacer(1, 6))
    story.append(Table([[""]], colWidths=[510], rowHeights=[10], style=[
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#2ecc71')),
    ]))
    story.append(Spacer(1, 12))

    # Extract the "Prescription Analysis" section from analysis_result
    prescription_analysis_text = ""
    if "1. Prescription Analysis:" in analysis_result:
        try:
            parts = re.split(r"1\. Prescription Analysis:", analysis_result, maxsplit=1)
            if len(parts) > 1:
                next_section = re.split(r"2\. Usage of Medicines:", parts[1], maxsplit=1)[0].strip()
                prescription_analysis_text = next_section
        except:
            prescription_analysis_text = "Not available"

    # Parse the Prescription Analysis text into a table
    table_data = parse_prescription_analysis_to_table(prescription_analysis_text)
    prescription_table = Table(table_data, colWidths=[170, 170, 170])
    prescription_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#FFFFFF')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, HexColor('#000000')),
    ]))
    story.append(prescription_table)
    story.append(Spacer(1, 24))

    # Analysis & Recommendations Section
    story.append(Paragraph("Analysis & Recommendations", styles['SubHeading']))
    story.append(Spacer(1, 6))
    story.append(Table([[""]], colWidths=[510], rowHeights=[10], style=[
        ('BACKGROUND', (0, 0), (-1, -1), HexColor('#2ecc71')),
    ]))
    story.append(Spacer(1, 12))

    # Parse analysis_result for specific sections
    sections = {
        "Problem Analysis": r"4\. Problem Analysis:",
        "Healthcare Tips": r"5\. Healthcare Tips:",
        "Physical Activity": r"6\. Physical Activity:",
        "Side Effects": r"7\. Side Effects:",
        "Food to Avoid": r"8\. Food to Avoid:",
        "Food to Prioritize": r"9\. Food to Prioritize:"
    }
    analysis_dict = {}
    for title, marker in sections.items():
        try:
            parts = re.split(marker, analysis_result, maxsplit=1)
            if len(parts) > 1:
                start_text = parts[1].strip()
                if title != "Food to Prioritize":
                    next_index = list(sections.keys()).index(title) + 1
                    if next_index < len(sections):
                        next_marker = list(sections.values())[next_index]
                        start_text = re.split(next_marker, start_text, maxsplit=1)[0].strip()
                analysis_dict[title] = clean_text(start_text)
            else:
                analysis_dict[title] = "Not available"
        except:
            analysis_dict[title] = "Not available"

    # Condition
    story.append(Paragraph("CONDITION:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Problem Analysis"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Glaucoma Care
    story.append(Paragraph("GLAUCOMA CARE:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Healthcare Tips"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Stomach Care
    story.append(Paragraph("STOMACH CARE:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Food to Avoid"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Exercise
    story.append(Paragraph("EXERCISE:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Physical Activity"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Side Effects (Added)
    story.append(Paragraph("SIDE EFFECTS:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Side Effects"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Food to Eat
    story.append(Paragraph("FOOD TO EAT:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Food to Prioritize"], styles['NormalText']))
    story.append(Spacer(1, 12))

    # Foods to Avoid
    story.append(Paragraph("FOODS TO AVOID:", styles['NormalText']))
    story.append(Paragraph(analysis_dict["Food to Avoid"], styles['NormalText']))
    story.append(Spacer(1, 24))

    # Add the disclaimer at the end of the story (ensures it appears on the last page)
    story.append(Paragraph("Disclaimer: This report is for informational purposes only. Please consult a healthcare professional for medical advice.", styles['FooterText']))

    # Footer (only page number on every page)
    def add_footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 10)
        canvas.setFillColor(HexColor('#000000'))
        canvas.drawString(72, 30, f"Confidential Report | Page {doc.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    return pdf_file

# Function to send email with PDF attachment
def send_email(to_email, pdf_file):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = "Your Medical Report"

    body = "Please find attached your medical report."
    msg.attach(MIMEText(body, 'plain'))

    with open(pdf_file, "rb") as f:
        part = MIMEApplication(f.read(), Name="report.pdf")
        part['Content-Disposition'] = 'attachment; filename="report.pdf"'
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Streamlit app layout
st.image("logo.png", width=150)

st.markdown("<h1 style='text-align: left;'><span style='color: #2ecc71;'>Medical Agent</span> - Prescription and Symptom Analysis</h1>", unsafe_allow_html=True)

# Input section on the left side
st.sidebar.header("User Inputs")
patient_name = st.sidebar.text_input("Patient Name:")
patient_age = st.sidebar.number_input("Patient Age:", min_value=0, max_value=150, step=1)
patient_sex = st.sidebar.selectbox("Patient Sex:", options=["", "Male", "Female"])
uploaded_file = st.sidebar.file_uploader("Upload Prescription (PDF/Image)", type=["pdf", "png", "jpg", "jpeg"])
user_problem = st.sidebar.text_area("Describe your problem or symptoms:")
user_allergy = st.sidebar.text_input("Any specific allergies?")

# Add "Get Report" button
get_report_clicked = st.sidebar.button("Get Report")

user_email = st.sidebar.text_input("Your Email Address:")

# Output section on the right side
st.header("Analysis Results")

# Initialize session state for analysis result and prescription text
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'prescription_text' not in st.session_state:
    st.session_state.prescription_text = None

# Process prescription and generate analysis when "Get Report" is clicked
if get_report_clicked:
    if not uploaded_file:
        st.warning("Please upload a prescription to continue.")
    else:
        with st.spinner("Processing prescription and generating report..."):
            prescription_text = ""
            
            if uploaded_file.type == "application/pdf":
                prescription_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type.startswith("image"):
                image = PILImage.open(uploaded_file)
                prescription_text = extract_text_from_image(image)
            else:
                st.error("Unsupported file type. Please upload a PDF or image.")
                st.stop()

            # Clean and filter the prescription text
            prescription_text = clean_text(prescription_text)

            # Store prescription_text in session state
            st.session_state.prescription_text = prescription_text

            # Prompt with strict formatting instructions
            prompt = f"""
            Prescription Data:
            {prescription_text}

            User Problem:
            {user_problem if user_problem else "Not provided"}

            User Allergy:
            {user_allergy if user_allergy else "Not provided"}

            Patient Details:
            Name: {patient_name if patient_name else "Not provided"}
            Age: {patient_age if patient_age else "Not provided"}
            Sex: {patient_sex if patient_sex else "Not provided"}

            Analyze the prescription, user problem, allergies, and patient details to determine the patient's likely medical condition. You MUST provide your response in the EXACT format below, using the numbered section headers as shown (e.g., '1. Prescription Analysis:'). Do not deviate from this structure, and ensure all sections are included, even if the content is minimal (e.g., write "Not enough information to analyze" if data is insufficient). Use the following structure:

            1. Prescription Analysis: Extract medicine names, dosage, and patient age if mentioned in the prescription.
            2. Usage of Medicines: Explain how and when to use each medicine.
            3. Medicine Details: Explain which medicine works for which problem (e.g., "Paracetamol is for pain relief and fever reduction").
            4. Problem Analysis: Identify the patient's likely medical condition based on the prescription, user problem, allergies, and patient details (e.g., "The patient likely has a fever or mild pain").
            5. Healthcare Tips: Suggest home remedies or natural remedies based on the identified condition.
            6. Physical Activity: Suggest exercises, physical activities, or rest based on the identified condition.
            7. Side Effects: Mention any side effects of the medicines.
            8. Food to Avoid: List specific food items to avoid based on the medical condition identified in "4. Problem Analysis". Provide a numbered list of at least 5 food items.
            9. Food to Prioritize: List specific food items that can help recovery based on the medical condition identified in "4. Problem Analysis". Provide a numbered list of at least 5 food items.

            Example 1 (for a fever condition):
            1. Prescription Analysis: Paracetamol 500mg, 1 tab TID; Patient age: 30
            2. Usage of Medicines: Paracetamol should be taken three times daily after meals.
            3. Medicine Details: Paracetamol is for pain relief and fever reduction.
            4. Problem Analysis: The patient likely has a fever or mild pain.
            5. Healthcare Tips: Drink plenty of water and rest.
            6. Physical Activity: Light walking is recommended; avoid strenuous exercise.
            7. Side Effects: Paracetamol may cause liver damage if overdosed.
            8. Food to Avoid: Avoid 1. alcohol 2. cigarettes 3. spicy food 4. fast food 5. oily food to support faster recovery from fever.
            9. Food to Prioritize: Eat 1. fruits (e.g., oranges) 2. leafy greens 3. soups 4. ginger tea 5. whole grains to aid recovery from fever.

            Example 2 (for hypertension):
            1. Prescription Analysis: Amlodipine 5mg, 1 tab OD; Patient age: 50
            2. Usage of Medicines: Amlodipine should be taken once daily in the morning.
            3. Medicine Details: Amlodipine is used to manage high blood pressure (hypertension).
            4. Problem Analysis: The patient likely has hypertension.
            5. Healthcare Tips: Reduce stress through meditation and maintain a regular sleep schedule.
            6. Physical Activity: Moderate exercise like brisk walking for 30 minutes daily is recommended.
            7. Side Effects: Amlodipine may cause dizziness or swelling in the ankles.
            8. Food to Avoid: Avoid 1. salty foods 2. processed meats 3. canned soups 4. fried foods 5. sugary drinks to manage hypertension.
            9. Food to Prioritize: Eat 1. bananas 2. spinach 3. oats 4. garlic 5. berries to help manage hypertension.

            Ensure each section is present and starts with the exact header as shown above (e.g., '1. Prescription Analysis:'). If you cannot identify the specific medical condition in "4. Problem Analysis", write "Not enough information to analyze the specific user problem" in that section, and provide general dietary recommendations in sections 8 and 9, clearly stating that they are not condition-specific.
            """

            try:
                model = genai.GenerativeModel('gemini-1.5-pro-002')
                response = model.generate_content(prompt)
                
                if not response.parts or response.candidates[0].finish_reason == 4:
                    st.error("The analysis could not be completed because the input may resemble copyrighted material. Please try rephrasing your problem or uploading a different prescription.")
                    full_text = "Analysis unavailable due to content restrictions."
                else:
                    full_text = response.text
                    st.write("Analysis generated successfully.")
                    print("DEBUG: full_text content:\n", full_text)

                st.session_state.analysis_result = full_text

            except genai.types.generation_types.BlockedPromptException as e:
                st.error(f"Analysis blocked: {e}")
                full_text = f"Error: {e}"
                st.session_state.analysis_result = full_text
            except Exception as e:
                if "429" in str(e):
                    st.error("API quota exceeded. Please try again later or check your API quota in Google Cloud Console.")
                    full_text = "Error: API quota exceeded."
                else:
                    st.error(f"An error occurred while calling the Gemini API: {e}")
                    full_text = f"Error: {e}"
                st.session_state.analysis_result = full_text

# Display cached analysis result if available
if st.session_state.analysis_result:
    full_text = st.session_state.analysis_result
    st.write("Displaying analysis result...")

    if "Error" not in full_text:
        sections = {
            "Prescription Analysis": r"1\. Prescription Analysis:",
            "Usage of Medicines": r"2\. Usage of Medicines:",
            "Medicine Details": r"3\. Medicine Details:",
            "Problem Analysis": r"4\. Problem Analysis:",
            "Healthcare Tips": r"5\. Healthcare Tips:",
            "Physical Activity": r"6\. Physical Activity:",
            "Side Effects": r"7\. Side Effects:",
            "Food to Avoid": r"8\. Food to Avoid:",
            "Food to Prioritize": r"9\. Food to Prioritize:"
        }

        for title, marker in sections.items():
            st.markdown(f"<h3 style='color: #2ecc71;'>{title}</h3>", unsafe_allow_html=True)
            try:
                parts = re.split(marker, full_text, maxsplit=1)
                if len(parts) > 1:
                    start_text = parts[1].strip()
                    if title != "Food to Prioritize":
                        next_index = list(sections.keys()).index(title) + 1
                        if next_index < len(sections):
                            next_marker = list(sections.values())[next_index]
                            start_text = re.split(next_marker, start_text, maxsplit=1)[0].strip()
                    st.write(start_text if start_text else "No content available for this section.")
                else:
                    st.write("Section not found in the response.")
            except Exception as e:
                st.write(f"Unable to parse this section: {str(e)}")

    # Send Report Button
    if user_email:
        if st.button("Send Report"):
            if 'prescription_text' in st.session_state and st.session_state.prescription_text:
                with st.spinner("Generating PDF and sending email..."):
                    pdf_file = generate_pdf_report(
                        st.session_state.prescription_text, 
                        user_problem, 
                        user_allergy, 
                        full_text,
                        patient_name,
                        patient_age,
                        patient_sex
                    )
                    if send_email(user_email, pdf_file):
                        st.success("Report sent successfully to your email!")
                    os.remove(pdf_file)
            else:
                st.error("Prescription text is not available. Please upload a prescription and click 'Get Report' first.")
    else:
        st.warning("Please enter your email address to send the report.")
else:
    st.info("Please upload a prescription and click 'Get Report' to see the analysis.")