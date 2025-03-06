import streamlit as st
import base64
import os

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
                #page-info {{
                    text-align: center;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div id="pdf-viewer"></div>
            <div class="nav-buttons">
                <button onclick="previousPage()">Previous</button>
                <button onclick="nextPage()">Next</button>
            </div>
            <div id="page-info">Page <span id="current-page"></span> of <span id="total-pages"></span></div>

            <script>
                const pdfData = "{pdf_base64}";
                let pdfDoc = null;
                let pageNum = {initial_page};
                let pageRendering = false;
                let pageNumPending = null;
                const scale = 1.0;

                const pdfViewer = document.getElementById('pdf-viewer');
                const currentPageSpan = document.getElementById('current-page');
                const totalPagesSpan = document.getElementById('total-pages');

                pdfjsLib.getDocument({{data: atob(pdfData)}}).promise.then(function(pdf) {{
                    pdfDoc = pdf;
                    totalPagesSpan.textContent = pdf.numPages;
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
                            currentPageSpan.textContent = num;
                            if (pageNumPending !== null) {{
                                renderPage(pageNumPending);
                                pageNumPending = null;
                            }}
                        }});
                    }});
                }}

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
    st.components.v1.html(pdf_js_code, height=950) # increased height

# Construct the PDF file path using os.path.join()
pdf_file_path = os.path.join("__pdf", "Grade08_Science_Chapter13.pdf")

if os.path.exists(pdf_file_path):
    # Convert the PDF to base64
    pdf_base64 = pdf_to_base64(pdf_file_path)

    # Display the PDF with an initial page
    display_pdf_with_pdfjs(pdf_base64, initial_page=3)  # Set the starting page as needed
else:
    st.error(f"PDF file not found at {pdf_file_path}")
