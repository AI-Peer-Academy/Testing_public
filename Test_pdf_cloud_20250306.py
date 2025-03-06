import streamlit as st
import base64
import os

def display_pdf_with_pdfjs(pdf_file_path, initial_page=1):
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')

    st.markdown(
        f"""
    <div id="pdf-viewer" style="width: 100%; height: 800px; overflow: auto;"></div>
    <div id="page-info" style="text-align: center; margin-top: 10px;">
        Page <span id="current-page">{initial_page}</span> of <span id="total-pages"></span>
    </div>
    <div style="display: flex; justify-content: center; margin-top: 10px;">
        <button onclick="previousPage()" style="margin: 0 10px;">Previous</button>
        <button onclick="nextPage()" style="margin: 0 10px;">Next</button>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
    <script>
        const pdfData = '{pdf_base64}';
        let pdfDoc = null;
        let pageNum = {initial_page};
        let pageRendering = false;
        let pageNumPending = null;
        const scale = 1.0;

        const pdfViewer = document.getElementById('pdf-viewer');
        const currentPageSpan = document.getElementById('current-page');
        const totalPagesSpan = document.getElementById('total-pages');

        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.worker.min.js';

        pdfjsLib.getDocument({{data: atob(pdfData)}}).promise.then(function(pdf) {{
            pdfDoc = pdf;
            totalPagesSpan.textContent = pdf.numPages;
            renderPage(pageNum);
        }}).catch(function(error) {{
            console.error("Error loading PDF:", error);
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
                }}).catch(function(error) {{
                    console.error("Error rendering page:", error);
                }});
            }}).catch(function(error) {{
                console.error("Error getting page:", error);
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
            currentPageSpan.textContent = pageNum;
        }}

        function previousPage() {{
            if (pageNum <= 1) return;
            pageNum--;
            queueRenderPage(pageNum);
            currentPageSpan.textContent = pageNum;
        }}
    </script>
    """,
        unsafe_allow_html=True,
    )

pdf_file_path = os.path.join("__pdf", "Grade08_Science_Chapter13.pdf")

if os.path.exists(pdf_file_path):
    display_pdf_with_pdfjs(pdf_file_path, initial_page=3)
else:
    st.error(f"PDF file not found at {pdf_file_path}")
