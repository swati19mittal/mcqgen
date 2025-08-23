import streamlit as st
from src.mcqgenerator.MCQGenerator import generate_mcqs
from mcqgenerator.parser import extract_text_from_pdf

st.title("MCQ Generator (LLM-powered)")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
num_q = st.slider("Number of Questions", 1, 10, 5)

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    text = extract_text_from_pdf("temp.pdf")
    st.subheader("Extracted Text Preview:")
    st.text_area("Text", text[:1000] + "..." if len(text) > 1000 else text, height=200)

    if st.button("Generate MCQs"):
        with st.spinner("Generating MCQs..."):
            mcqs = generate_mcqs(text, num_q)
        st.subheader("Generated MCQs:")
        st.write(mcqs)
