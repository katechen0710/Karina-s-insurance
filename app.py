import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="阿圓的保險分析", layout="wide")

# ===== 主視覺 =====
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>🐶 阿圓的保險分析</h1>
<p style='text-align: center;'>上傳你的保險合約，快速找出關鍵條款</p>
""", unsafe_allow_html=True)

# 狗狗圖片（白色狗）
st.image("https://images.unsplash.com/photo-1558788353-f76d92427f16", use_container_width=True)

st.divider()

# Upload PDF file
uploaded_file = st.file_uploader("📄 Upload your contract (PDF only)", type=["pdf"])

# Keyword input
keyword = st.text_input("🔍 Enter keyword to search clauses")

# Extract text safely from PDF
def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Find keyword with context
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

    if not text.strip():
        st.warning("⚠️ This PDF may be scanned or contains no readable text.")
    else:
        if keyword:
            results = find_keyword_clauses(text, keyword)

            if results:
                st.success(f"✅ Found {len(results)} matching clauses:")
                for i, res in enumerate(results, 1):
                    st.markdown(f"### 📌 Result {i}")
                    st.text(res)
                    st.divider()
            else:
                st.warning("❌ No matching clauses found.")
        else:
            st.info("💡 Please enter a keyword to search.")
else:
    st.info("⬆️ Please upload a PDF file to begin.")

# Footer
st.caption("🐾 Built with Streamlit | 阿圓守護你的合約")
