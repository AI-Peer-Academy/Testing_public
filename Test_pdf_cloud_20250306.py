import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os

def open_pdfViewer(pdf_file, page_number=2):
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
if "page_number" not in st.session_state:
    st.session_state.page_number = 1

# Example usage
st.title("PDF Viewer")
#open_pdfViewer("example.pdf", st.session_state.page_number)

open_pdfViewer("Grade08_Science_Chapter13.pdf")

