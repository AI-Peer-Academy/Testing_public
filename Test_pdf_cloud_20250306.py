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

# File uploader to load the PDF
pdf_file = st.file_uploader("Upload PDF", type="pdf")
if pdf_file:
    # Save the uploaded file temporarily
    pdf_path = f"__pdf/{pdf_file.name}"
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    # Convert the PDF to base64
    pdf_base64 = pdf_to_base64(pdf_path)

    # Display the PDF with an initial page
    display_pdf_with_pdfjs(pdf_base64, initial_page=3)  # Set the starting page as needed
else:
    st.warning("Please upload a PDF file.")
