import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Contract Reader", layout="wide")

st.title("📄 Contract Keyword Extractor")
st.write("Upload a PDF contract and search for specific clauses using keywords.")

# Upload PDF file
uploaded_file = st.file_uploader("Upload your contract (PDF only)", type=["pdf"])

# Keyword input
keyword = st.text_input("Enter keyword to search clauses")

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to find keyword context
def find_keyword_clauses(text, keyword):
    results = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            context = "\n".join(lines[max(0, i-2): min(len(lines), i+3)])
            results.append(context)
    return results

# Main logic
if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)

    if keyword:
        results = find_keyword_clauses(text, keyword)

        if results:
            st.success(f"Found {len(results)} matching clauses:")
            for i, res in enumerate(results, 1):
                st.markdown(f"### Result {i}")
                st.write(res)
                st.divider()
        else:
            st.warning("No matching clauses found.")
    else:
        st.info("Please enter a keyword to search.")
else:
    st.info("Please upload a PDF file.")

# Footer
st.caption("Built with Streamlit + PyPDF2")
