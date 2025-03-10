#20250306 23:00 works
import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import os

# Ensure session state is initialized for page tracking
if "page_number" not in st.session_state:
    st.session_state.page_number = 3

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
