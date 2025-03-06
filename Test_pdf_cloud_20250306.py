import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import base64

import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import os

# Ensure session state is initialized for page tracking
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# Function to render PDF page as an image
def open_pdfViewer_as_image(pdf_file, page_number=2):
    try:
        pdf_folder = "__pdf"
        pdf_path = os.path.join(pdf_folder, pdf_file)

        # Check if the PDF file exists
        if not os.path.exists(pdf_path):
            st.error("PDF file not found.")
            return

        # Open the PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        # Validate page number
        if page_number < 1 or page_number > total_pages:
            st.error("Invalid page number.")
            return

        # Render the selected page as an image
        page = doc[page_number - 1]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Display the image in Streamlit
        st.image(img, caption=f"Page {page_number} of {total_pages}", use_column_width=True)

        # Page navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Previous", key="prev"):
                st.session_state.page_number = max(1, st.session_state.page_number - 1)
        with col2:
            if st.button("Next ➡️", key="next"):
                st.session_state.page_number = min(total_pages, st.session_state.page_number + 1)

    except Exception as e:
        st.error(f"Error displaying PDF page: {e}")

# Upload PDF file for testing
uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_pdf is not None:
    # Save the uploaded PDF to the __pdf folder
    pdf_folder = "__pdf"
    if not os.path.exists(pdf_folder):
        os.makedirs(pdf_folder)

    # Save the uploaded PDF file
    with open(os.path.join(pdf_folder, uploaded_pdf.name), "wb") as f:
        f.write(uploaded_pdf.getbuffer())

    # Open the uploaded PDF using the saved file and current page from session state
    open_pdfViewer_as_image(uploaded_pdf.name, st.session_state.page_number)



def gdrive_pdf():
    # Google Drive file ID
    file_id = "1CMU4xK3u_wAGD0Ev_YsV-shC88ujXi83"
    
    # Set default page number
    default_page = 5
    page_number = st.number_input("Go to page:", min_value=1, value=default_page, step=1)
    
    # Use Google Docs Viewer instead of Google Drive
    pdf_viewer_url = f"https://docs.google.com/gview?url=https://drive.google.com/uc?id={file_id}&embedded=true#page={page_number}"
    
    # Open in a new tab
    st.markdown(f"[Open PDF (Page {page_number})]({pdf_viewer_url})", unsafe_allow_html=True)



def open_pdfViewer_as_image(pdf_file, page_number=2):
    try:
        pdf_folder = "__pdf"
        pdf_path = os.path.join(pdf_folder, pdf_file)

        if not os.path.exists(pdf_path):
            st.error("PDF file not found.")
            return

        # Open the PDF
        doc = fitz.open(pdf_path)
        total_pages = len(doc)

        if page_number < 1 or page_number > total_pages:
            st.error("Invalid page number.")
            return

        # Render the selected page as an image
        page = doc[page_number - 1]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Display the image in Streamlit
        st.image(img, caption=f"Page {page_number} of {total_pages}", use_column_width=True)

        # Page navigation buttons
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("⬅️ Previous", key="prev"):
                st.session_state.page_number = max(1, page_number - 1)
        with col2:
            if st.button("Next ➡️", key="next"):
                st.session_state.page_number = min(total_pages, page_number + 1)

    except Exception as e:
        st.error(f"Error displaying PDF page: {e}")

# Initialize session state for page tracking
#if "page_number" not in st.session_state:
#    st.session_state.page_number = 1

# Example usage
#st.title("PDF Viewer")
#open_pdfViewer("example.pdf", st.session_state.page_number)

#open_pdfViewer("Grade08_Science_Chapter13.pdf")

