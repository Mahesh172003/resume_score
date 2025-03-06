import streamlit as st
import PyPDF2
from nltk.tokenize import word_tokenize
import nltk
import re

# Download NLTK data (run once)
nltk.download('punkt')

# Function to extract text from PDF resume
def extract_resume_text(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Function to clean and extract keywords
def get_keywords(text):
    # Basic cleaning: lowercase, remove special chars
    text = re.sub(r'[^\w\s]', '', text.lower())
    tokens = word_tokenize(text)
    # Filter for meaningful words (e.g., longer than 3 chars)
    keywords = {word for word in tokens if len(word) > 3 and word.isalpha()}
    return keywords

# Function to score resume and generate suggestions
def score_resume(resume_text, job_desc):
    if not resume_text or not job_desc:
        return 0, "Please provide both resume and job description."
    
    job_keywords = get_keywords(job_desc)
    resume_keywords = get_keywords(resume_text)
    
    # Calculate match score
    matches = job_keywords.intersection(resume_keywords)
    score = (len(matches) / len(job_keywords)) * 100 if job_keywords else 0
    
    # Generate suggestions
    missing_keywords = job_keywords - resume_keywords
    if missing_keywords:
        suggestions = f"Consider adding these keywords: {', '.join(missing_keywords)}"
    else:
        suggestions = "Great match! No major suggestions."
    
    return round(score, 2), suggestions

# Streamlit UI
def main():
    st.title("Resume Scoring Prototype")
    st.write("Upload your resume and enter a job description to get a match score and suggestions!")

    # Input section
    st.subheader("Input")
    resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    job_desc = st.text_area("Paste Job Description Here", height=150)

    # Process and display output
    if st.button("Score My Resume"):
        if resume_file and job_desc:
            with st.spinner("Analyzing..."):
                resume_text = extract_resume_text(resume_file)
                score, suggestions = score_resume(resume_text, job_desc)
                
                # Output section
                st.subheader("Results")
                st.write(f"**Resume Match Score**: {score}%")
                st.write(f"**Suggestions**: {suggestions}")
        else:
            st.error("Please upload a resume and enter a job description.")

if __name__ == "__main__":
    main()
