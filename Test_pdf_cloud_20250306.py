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
      <head>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.10.377/pdf.min.js"></script>
          <style>
              #pdf-viewer {{
                  width: 100%;
                  height: 800px;
                  overflow: auto;
              }}
              .nav-area {{
                  display: flex;
                  justify-content: space-around; /* Distribute space evenly */
                  align-items: center; /* Vertically align items */
                  margin-top: 10px;
              }}
              .nav-buttons button, .page-input-area button {{ /* Style for all buttons */
                  margin: 0 5px;
              }}
              .page-input-area {{
                  display: flex;
                  align-items: center;
              }}
              .page-input-area input {{
                  width: 70px; /* Adjust width as needed */
                  margin: 0 5px;
                  text-align: center;
              }}
          </style>
      </head>
  <body>
      <div class="nav-area">
          <div class="nav-buttons">
              <button onclick="previousPage()">Previous</button>
              <button onclick="nextPage()">Next</button>
          </div>
          <div class="page-info">
              <span id="current-page"></span> / <span id="total-pages"></span>
          </div>
          <div class="page-input-area">
              <input type="number" id="page-number-input" min="1">
              <button onclick="goToPage()">Go to Page</button>
          </div>
      </div>
  
      <div id="pdf-viewer"></div>
  
  
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
          const pageNumberInput = document.getElementById('page-number-input');
  
  
          pdfjsLib.getDocument({{data: atob(pdfData)}}).promise.then(function(pdf) {{
              pdfDoc = pdf;
              setTimeout(function() {{ // Added setTimeout for total pages
                  totalPagesSpan.textContent = pdfDoc.numPages; // Display total pages
              }}, 100);
              pageNumberInput.max = pdfDoc.numPages;       // Set max for input
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
                      currentPageSpan.textContent = num; // Update current page display
                      pageNumberInput.value = num;        // Update input value to current page
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
  
          function goToPage() {{
              let pageToGo = parseInt(pageNumberInput.value);
              if (pageToGo >= 1 && pageToGo <= pdfDoc.numPages) {{
                  pageNum = pageToGo;
                  queueRenderPage(pageNum);
              }} else {{
                  alert("Invalid page number. Please enter a page between 1 and " + pdfDoc.numPages);
                  pageNumberInput.value = pageNum; // Revert input to current page
              }}
          }}
  
  
      </script>
  </body>
  </html>
  """
  # Embed the HTML/JS into Streamlit
  st.components.v1.html(pdf_js_code, height=950) # Increased height to accommodate new elements

# File uploader to load the PDF
#pdf_file_path = "__pdf/Grade08_Science_Chapter13.pdf"  # Fixed path to the PDF
# Construct the PDF file path using os.path.join()
pdf_file_path = os.path.join("__pdf", "Grade08_Science_Chapter13.pdf")

#if os.path.exists(pdf_file_path):
#  # Convert the PDF to base64
pdf_base64 = pdf_to_base64(pdf_file_path)
#  # Display the PDF with an initial page
display_pdf_with_pdfjs(pdf_base64, initial_page=3)# Set the starting page as needed
#else:
#  st.error(f"PDF file not found at {pdf_file_path}")
