import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
#import gdown
import os
import base64

#pdf_url = "https://drive.google.com/file/d/1CMU4xK3u_wAGD0Ev_YsV-shC88ujXi83/view?usp=sharing"

import streamlit as st
import streamlit.components.v1 as components
import base64

def display_pdf_with_page(pdf_file, page_num):
    """Displays a PDF with a specific page number in Streamlit."""

    with open(pdf_file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page={page_num}" width="800" height="800" type="application/pdf"></iframe>'

    st.markdown(pdf_display, unsafe_allow_html=True)

# Example usage:
#pdf_file_path = "__pdf\Grade08_Science_Chapter13.pdf"  # Replace with your PDF file path
pdf_file_path = os.path.join("__pdf", "Grade08_Science_Chapter13.pdf")
page_to_open = 2  # Specify the page number you want to open

try:
    display_pdf_with_page(pdf_file_path, page_to_open)
except FileNotFoundError:
    st.error(f"File not found: {pdf_file_path}")
except Exception as e:
    st.error(f"An error occurred: {e}")
    
#open_pdfViewer("Grade08_Science_Chapter13.pdf")

