import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(page_title="AI Worksheet Generator", layout="centered")

st.title("📝 AI Worksheet & Question Paper Generator")
st.write("Upload a chapter photo, set requirements, and generate a worksheet instantly.")

uploaded_file = st.file_uploader("Upload Chapter Image", type=["jpg", "jpeg", "png"])

col1, col2 = st.columns(2)
with col1:
    mcqs = st.slider("Multiple Choice (MCQs)", 0, 10, 5)
    t_f = st.slider("True / False", 0, 10, 5)
with col2:
    blanks = st.slider("Fill in the Blanks", 0, 10, 5)
    long_qs = st.slider("Question & Answers", 0, 5, 2)

api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key", type="password")

if st.button("✨ Generate Worksheet", type="primary"):
    if not uploaded_file:
        st.error("Please upload an image first!")
    elif not api_key:
        st.error("Please provide a Gemini API Key.")
    else:
        with st.spinner("Analyzing chapter and generating worksheet..."):
            try:
                client = genai.Client(api_key=api_key)
                img = Image.open(uploaded_file)
                
                prompt = f"""
                You are an expert school teacher. Analyze the attached textbook image completely.
                Based strictly on the content found in the image, generate a clean worksheet containing:
                1. {mcqs} Multiple Choice Questions (with options A, B, C, D)
                2. {t_f} True or False statements
                3. {blanks} Fill in the Blanks questions
                4. {long_qs} Short/Long Answer Questions (with model answers)
                
                Provide a clear "Answer Key" at the very bottom for items 1, 2, and 3.
                Formatting: Use bold text for headers and clear spacing.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[img, prompt]
                )
                
                st.success("Worksheet Generated!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
