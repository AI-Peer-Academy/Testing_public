import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import base64

import streamlit as st
import base64

# Function to convert the PDF file (from a fixed path or URL) to base64
def pdf_to_base64(pdf_file_path):
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
    return base64.b64encode(pdf_data).decode('utf-8')

# Function to display the PDF using PDF.js
def display_pdf_with_pdfjs(pdf_base64, initial_page=1):
    pdf_js_code = f"""
    <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
            <style>
                #pdf-viewer {{
                    width: 100%;
                    height: 800px;
                    overflow: auto;
                }}
                .nav-buttons {{
                    display: flex;
                    justify-content: center;
                    margin-top: 10px;
                }}
                .nav-buttons button {{
                    margin: 0 10px;
                }}
            </style>
        </head>
        <body>
            <div id="pdf-viewer"></div>
            <div class="nav-buttons">
                <button onclick="previousPage()">Previous</button>
                <button onclick="nextPage()">Next</button>
            </div>

            <script>
                const pdfData = "{pdf_base64}";
                let pdfDoc = null;
                let pageNum = {initial_page};
                let pageRendering = false;
                let pageNumPending = null;
                const scale = 1.0;

                const pdfViewer = document.getElementById('pdf-viewer');

                pdfjsLib.getDocument({{data: atob(pdfData)}}).promise.then(function(pdf) {{
                    pdfDoc = pdf;
                    renderPage(pageNum);
                }});

                function renderPage(num) {{
                    pageRendering = true;
                    pdfDoc.getPage(num).then(function(page) {{
                        const viewport = page.getViewport({{scale: scale}});
                        const canvas = document.createElement('canvas');
                        const context = canvas.getContext('2d');
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        pdfViewer.innerHTML = '';
                        pdfViewer.appendChild(canvas);

                        const renderContext = {{
                            canvasContext: context,
                            viewport: viewport
                        }};
                        page.render(renderContext).promise.then(function() {{
                            pageRendering = false;
                            if (pageNumPending !== null) {{
                                renderPage(pageNumPending);
                                pageNumPending = null;
                            }}
                        }});
                    }});
                }

                function queueRenderPage(num) {{
                    if (pageRendering) {{
                        pageNumPending = num;
                    }} else {{
                        renderPage(num);
                    }}
                }}

                function nextPage() {{
                    if (pageNum >= pdfDoc.numPages) return;
                    pageNum++;
                    queueRenderPage(pageNum);
                }}

                function previousPage() {{
                    if (pageNum <= 1) return;
                    pageNum--;
                    queueRenderPage(pageNum);
                }}
            </script>
        </body>
    </html>
    """
    # Embed the HTML/JS into Streamlit
    st.components.v1.html(pdf_js_code, height=900)

# Specify a fixed PDF file path or URL
#pdf_file_path = "path/to/your/fixed/pdf_file.pdf"  # Replace with the correct path to your file
pdf_folder = "__pdf"
pdf_path = os.path.join(pdf_folder, pdf_file)

# Convert the PDF to base64
pdf_base64 = pdf_to_base64(pdf_file_path)

# Display the PDF with an initial page of your choice
display_pdf_with_pdfjs(pdf_base64, initial_page=3)  # You can set any starting page number


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

