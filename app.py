import streamlit as st
from PyPDF2 import PdfReader
import re

st.set_page_config(page_title="阿圓的保險分析", layout="wide")

# ===== 主視覺 =====
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>🐶 阿圓的保險分析</h1>
<p style='text-align: center;'>上傳你的保險合約，快速找出關鍵條款</p>
""", unsafe_allow_html=True)


uploaded_file = st.file_uploader("📄 Upload your contract (PDF only)", type=["pdf"])
keyword = st.text_input("🔍 Enter keyword to search clauses")

# ===== 擷取 PDF（保留頁碼） =====
def extract_text_by_page(file):
    pages_data = []
    try:
        reader = PdfReader(file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages_data.append({
                    "page": i + 1,
                    "text": text
                })
        return pages_data
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return []

# ===== 嘗試抓「條款編號」 =====
def extract_clauses(text):
    # 常見條款格式：1. / 1.1 / 第1條
    pattern = r"(第\s*\d+\s*條|\d+\.\d+|\d+\.)"
    splits = re.split(pattern, text)

    clauses = []
    current_clause = ""

    for part in splits:
        if re.match(pattern, part):
            if current_clause:
                clauses.append(current_clause.strip())
            current_clause = part
        else:
            current_clause += " " + part

    if current_clause:
        clauses.append(current_clause.strip())

    return clauses

# ===== 搜尋 =====
def search_keyword(pages_data, keyword):
    results = []

    for page_data in pages_data:
        page_num = page_data["page"]
        text = page_data["text"]

        clauses = extract_clauses(text)

        for clause in clauses:
            if keyword.lower() in clause.lower():
                results.append({
                    "page": page_num,
                    "clause": clause
                })

    return results

# ===== 主邏輯 =====
if uploaded_file is not None:
    pages_data = extract_text_by_page(uploaded_file)

    if not pages_data:
        st.warning("⚠️ This PDF may be scanned or contains no readable text.")
    else:
        if keyword:
            results = search_keyword(pages_data, keyword)

            if results:
                st.success(f"✅ Found {len(results)} matching clauses:")

                for i, res in enumerate(results, 1):
                    st.markdown(f"### 📌 Result {i}")
                    st.markdown(f"**📄 Page:** {res['page']}")
                    st.markdown("**📑 Clause:**")
                    st.write(res['clause'])
                    st.divider()
            else:
                st.warning("❌ No matching clauses found.")
        else:
            st.info("💡 Please enter a keyword to search.")
else:
    st.info("⬆️ Please upload a PDF file to begin.")

st.caption("🐾 Built with Streamlit | 阿圓守護你的合約")
