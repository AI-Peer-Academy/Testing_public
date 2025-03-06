import streamlit as st

def display_pdf_with_pdfjs(pdf_url):
    pdf_js_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF.js Viewer from Google Drive (with Page Navigation)</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
        <style>
            #pdf-viewer {{
                width: 100%;
                height: 600px;
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
            const pdfUrl = "{pdf_url}";
            let pdfDoc = null;
            let pageNum = 1;
            let pageRendering = false;
            let pageNumPending = null;
            const scale = 1.5;

            const pdfViewer = document.getElementById('pdf-viewer');

            pdfjsLib.getDocument(pdfUrl).promise.then(function(pdf) {{
                pdfDoc = pdf;
                renderPage(pageNum);
            }});

            function renderPage(num) {{
                pageRendering = true;
                pdfDoc.getPage(num).then(function(page) {{
                    const viewport = page.getViewport({{ scale: scale }});
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    pdfViewer.innerHTML = '';
                    pdfViewer.appendChild(canvas);

                    page.render({{ canvasContext: context, viewport: viewport }}).promise.then(function() {{
                        pageRendering = false;
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
    st.components.v1.html(pdf_js_code, height=700)

pdf_url = "https://drive.google.com/uc?id=1CMU4xK3u_wAGD0Ev_YsV-shC88ujXi83"  # Replace with your Google Drive PDF URL
display_pdf_with_pdfjs(pdf_url)
