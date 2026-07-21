import streamlit as st
from google import genai
from PIL import Image
from fpdf import FPDF

st.set_page_config(page_title="AI Worksheet Generator", layout="centered")

st.title("📝 AI Worksheet & Question Paper Generator")
st.write("Upload 1 or more chapter photos, set requirements, and generate a complete worksheet instantly.")

uploaded_files = st.file_uploader(
    "Upload Chapter Images (Select 1 to 5 photos)", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

col1, col2 = st.columns(2)
with col1:
    mcqs = st.slider("Multiple Choice (MCQs)", 0, 10, 5)
    t_f = st.slider("True / False", 0, 10, 5)
with col2:
    blanks = st.slider("Fill in the Blanks", 0, 10, 5)
    long_qs = st.slider("Question & Answers", 0, 5, 2)

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

def create_pdf(text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)
    
    # Handle utf-8 encoding safely for basic text
    for line in text_content.split("\n"):
        # Encode string to latin-1 compatible for FPDF default font
        clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, txt=clean_line)
    
    return bytes(pdf.output())

if st.button("✨ Generate Worksheet", type="primary"):
    if not uploaded_files:
        st.error("Please upload at least one image first!")
    elif not api_key:
        st.error("Please provide a Gemini API Key.")
    else:
        with st.spinner(f"Analyzing {len(uploaded_files)} image(s) and generating worksheet..."):
            try:
                client = genai.Client(api_key=api_key)
                images = [Image.open(file) for file in uploaded_files]
                
                # Updated prompt for strict line breaks on options A, B, C, D
                prompt = f"""
                You are an expert school teacher. Analyze all the attached textbook images completely as a continuous chapter/lesson.
                Based strictly on the content found across all these images, generate a clean worksheet containing:

                1. {mcqs} Multiple Choice Questions. 
                   CRITICAL FORMATTING FOR MCQS:
                   Put the question text on its own line.
                   Put EACH option (A, B, C, D) on a NEW LINE directly below the question. 
                   Example:
                   1. What is the main source of light?
                   A) Sun
                   B) Moon
                   C) Lamp
                   D) Candle

                2. {t_f} True or False statements
                3. {blanks} Fill in the Blanks questions
                4. {long_qs} Short/Long Answer Questions (with model answers)
                
                Provide a clear "Answer Key" at the very bottom for items 1, 2, and 3.
                Formatting: Use clear headers and line spacing.
                """
                
                contents = [prompt] + images
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents
                )
                
                st.success("Worksheet Generated!")
                
                worksheet_text = response.text
                st.markdown(worksheet_text)
                
                # Generate PDF binary data
                pdf_bytes = create_pdf(worksheet_text)
                
                # Add PDF Download Button
                st.download_button(
                    label="📄 Download Worksheet as PDF",
                    data=pdf_bytes,
                    file_name="generated_worksheet.pdf",
                    mime="application/pdf",
                    type="primary"
                )
                
            except Exception as e:
                st.error(f"Error: {e}")
