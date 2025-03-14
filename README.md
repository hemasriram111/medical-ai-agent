# Medical Agent - Prescription and Symptom Analysis

## self introduction

Hi, I’m **Hema Sriram**, an aspiring **AI and Machine Learning Engineer** with a strong foundation in **deep learning, NLP, and cloud technologies**. I’m currently pursuing my B.Tech in AI & ML . During my internship at **Technical Hub - Generative AI**, I worked on **OpenCV, NLP, and CNN models**, contributing to real-world AI solutions. I’ve built projects like the **Cold Email Generator using Llama 3.1**, the **LangChain-PDF Bot**, and a **Resume Analyzer**, showcasing my skills in **generative AI, RAG, and semantic search**. Certified in **Google Cloud, Oracle AI, and IBM AI Fundamentals**, I’m passionate about leveraging AI to solve complex problems and thrive in collaborative environments.

## problem statement 

As i observed grow stack ai agent there is no medical field medical ai agent  it makes me feel that would be best choice use this field as  every one not familiar with every tablet they use . most of educated one don't know which tablet works for which problem and what are the side effects that cause also worry about which food should take and which to avoid this problem can be cleared with this one single ai agent 

## Overview
The **Medical Agent** is an AI-powered application designed to assist users in analyzing medical prescriptions and symptoms. Built for **Grow Stack**, this tool leverages advanced technologies like **Google Gemini API**, **Tesseract OCR**, and **Streamlit** to provide a seamless experience for users to upload prescriptions, describe symptoms, and receive detailed medical analysis. The application also generates a comprehensive PDF report and sends it via email, making it a valuable tool for both patients and healthcare professionals.

---

## Significance of the AI Agent
In today's fast-paced world, managing medical prescriptions and understanding symptoms can be challenging. The **Medical Agent** simplifies this process by:
1. **Automating Prescription Analysis**: Extracts and interprets prescription details using OCR and AI.
2. **Providing Personalized Insights**: Analyzes symptoms, allergies, and patient details to offer tailored recommendations.
3. **Enhancing Accessibility**: Generates easy-to-understand reports and sends them directly to the user's email.
4. **Improving Healthcare Efficiency**: Reduces the time and effort required for manual prescription analysis and symptom interpretation.

This AI agent is a perfect fit for **Grow Stack** as it aligns with the company's mission to innovate and provide cutting-edge solutions that improve user experiences and outcomes.

---

## Key Features

### 1. **Prescription Upload and Analysis**
   - **Supported Formats**: Users can upload prescriptions in **PDF** or **image formats** (PNG, JPG, JPEG).
   - **Text Extraction**: The app uses **Tesseract OCR** to extract text from images and **PyPDF2** for PDF files.
   - **Cleaning and Filtering**: Extracted text is cleaned to remove unnecessary characters and formatting.

### 2. **Symptom and Allergy Input**
   - Users can describe their symptoms and specify any allergies.
   - This information is combined with the prescription data for a comprehensive analysis.

### 3. **AI-Powered Medical Analysis**
   - The **Google Gemini API** is used to analyze the prescription, symptoms, and patient details.
   - The analysis includes:
     - **Prescription Details**: Medicine names, dosage, and frequency.
     - **Usage Instructions**: How and when to take each medicine.
     - **Problem Analysis**: Likely medical conditions based on the input.
     - **Healthcare Tips**: Home remedies and natural solutions.
     - **Physical Activity Recommendations**: Exercises or rest suggestions.
     - **Side Effects**: Potential side effects of prescribed medicines.
     - **Dietary Recommendations**: Foods to avoid and prioritize for recovery.

### 4. **Interactive User Interface**
   - Built using **Streamlit**, the app provides an intuitive and user-friendly interface.
   - Users can input their details, upload prescriptions, and view analysis results in real-time.

### 5. **PDF Report Generation**
   - The app generates a professional **PDF report** using **ReportLab**.
   - The report includes:
     - Patient information.
     - Prescription analysis in a tabular format.
     - Detailed medical analysis and recommendations.
     - A disclaimer for informational purposes.

### 6. **Email Integration**
   - Users can enter their email address to receive the PDF report.
   - The app uses **SMTP** to send the report as an email attachment.


## How It Works
1. **User Inputs**:
   - Enter patient details (name, age, sex).
   - Upload a prescription (PDF or image).
   - Describe symptoms and specify allergies.
2. **Analysis**:
   - The app extracts and cleans text from the prescription.
   - The Google Gemini API analyzes the data and generates insights.
3. **Report Generation**:
   - A PDF report is created with the analysis results.
4. **Email Delivery**:
   - The report is sent to the user's email address.

---

## Technology Stack
- **Frontend**: Streamlit( analysed growstack ai agents interface and implimented simillarly)
- **Backend**: Python
- **OCR**: Tesseract
- **PDF Processing**: PyPDF2
- **PDF Generation**: ReportLab (used grow stack colur pallet to make ui more engaging and simp;e)
- **AI Model**: Google Gemini API
- **Email Integration**: SMTP (smtplib)

---

## Installation and Setup


1. ```bash
   git clone https://github.com/hemasriram111/medical-ai-agent.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Google Gemini API:
   - Replace the `api_key` in the code with your Google Gemini API key.
4. Configure Email:
   - Replace `EMAIL_ADDRESS` and `EMAIL_PASSWORD` with your email credentials.
5. Run the app:
 
6. ```bash
   streamlit run app.py
   ```


---

## Future Enhancements
- **Multi-Language Support**: Add support for prescriptions in multiple languages.
- **Mobile App Development**: Create a mobile version for better accessibility.

---

## Disclaimer
This application is for **informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

---

## Contact
For any queries or feedback, please contact:
- **Name**: Hema sriram
- **Email**: hemasriram111@gmail.com
- **LinkedIn**: https://www.linkedin.com/in/hemasriram/

## More information 
Confidential information, such as the Google AI Studio API key, Google Mail, and its SMTP password, remains included in the code. This was done for the sake of fast evaluation and testing of the application.

in case of any queries regarding agent contact at any time 

