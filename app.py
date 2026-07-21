import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Worksheet Generator", layout="centered")

st.title("📝 AI Worksheet & Question Paper Generator")
st.write("Upload 1 or more chapter photos, set requirements, and generate a complete worksheet instantly.")

# Enable uploading multiple files at once
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

if st.button("✨ Generate Worksheet", type="primary"):
    if not uploaded_files:
        st.error("Please upload at least one image first!")
    elif not api_key:
        st.error("Please provide a Gemini API Key.")
    else:
        with st.spinner(f"Analyzing {len(uploaded_files)} image(s) and generating worksheet..."):
            try:
                client = genai.Client(api_key=api_key)
                
                # Convert all uploaded files into PIL Images
                images = [Image.open(file) for file in uploaded_files]
                
                prompt = f"""
                You are an expert school teacher. Analyze all the attached textbook images completely as a continuous chapter/lesson.
                Based strictly on the content found across all these images, generate a clean worksheet containing:
                1. {mcqs} Multiple Choice Questions (with options A, B, C, D)
                2. {t_f} True or False statements
                3. {blanks} Fill in the Blanks questions
                4. {long_qs} Short/Long Answer Questions (with model answers)
                
                Provide a clear "Answer Key" at the very bottom for items 1, 2, and 3.
                Formatting: Use bold text for headers and clear spacing.
                """
                
                # Pass prompt along with the list of images to Gemini
                contents = [prompt] + images
                
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=contents
                )
                
                st.success("Worksheet Generated!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
