import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import gdown
import os
import base64

#pdf_url = "https://drive.google.com/file/d/1CMU4xK3u_wAGD0Ev_YsV-shC88ujXi83/view?usp=sharing"

def open_pdfViewer(pdf_file):

    try:
        pdf_folder = os.path.abspath('__pdf')
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print("PDF path:", pdf_path)
        # Extract the file ID from the URL
        #file_id = pdf_url.split('/')[-2]

        # Download the file using gdown
        output_file = 'temp.pdf'  # Temporary file name
        #gdown.download(id=file_id, output=output_file, quiet=False)

        # Open the downloaded file in binary mode
        #with open(output_file, 'rb') as f:
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()  # Read the raw bytes

        # Display the PDF
        pdf_viewer(pdf_bytes, width=700)

    except Exception as e:
        st.error(f"Error downloading or displaying PDF: {e}")

def open_pdfBrowser(pdf_file):
    #import streamlit as st

    #pdf_file = "path/to/your_file.pdf"  # Ensure this file is accessible (e.g., hosted or in the static folder)
    page_number = 3  # The page you want to open

    # Append the page fragment to the URL
    pdf_url = f"{pdf_file}#page={page_number}"

    # Embed the PDF using an iframe
    st.markdown(
        f'<iframe src="{pdf_url}" width="700" height="900"></iframe>',
        unsafe_allow_html=True
    )

def old_open_pdfBase64(chunk_id, page): #Looks perfect, goes into the page.
    #chunk_id = 'Grade08_Science_Chapter13_Chunk06'

    # Split the chunk_id at the underscores
    parts = chunk_id.split('_')

    # Extract the grade, subject, and chapter if available
    if len(parts) >= 3:
        grade = parts[0]  # Grade08
        subject = parts[1]  # Science
        chapter_number = parts[2]  # Chapter13
        print(grade, subject, chapter_number)
    else:
        print("Invalid chunk_id format")

    if subject.lower() == "science":
        pdf_file = f"{grade}_{subject}_{chapter_number}.pdf"
        pdf_file = "/__pdf/" + pdf_file
        print(pdf_file)  # Output: Grade08_Science_Chapter01.pdf
        # Get the absolute path of the __pdf folder
        pdf_folder = os.path.abspath('__pdf')

        # Construct the full path to the PDF file
        pdf_path = os.path.join(pdf_folder, 'Grade08_Science_Chapter13.pdf')
        print((pdf_path))

    def get_pdf_base64(file_path):
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        return base64.b64encode(pdf_bytes).decode("utf-8")

    # Adjust the path to your PDF relative to the script
    #pdf_file = "pdf/temp.pdf"
    #base64_pdf = get_pdf_base64(pdf_file)
    base64_pdf = get_pdf_base64(pdf_path)
    page = 3  # Example page number
    pdf_display = f'''
    <div style="display: flex; justify-content: center; width: 100%;">
        <iframe src="data:application/pdf;base64,{base64_pdf}#page={page}" 
                style="width: 70%; height: 1200px;" frameborder="0">
        </iframe>
    </div>
    '''

    st.markdown(pdf_display, unsafe_allow_html=True)
    # Embed the PDF using a data URL
    #pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}#page=3" width="700" height="900"></iframe>'
    
    #pdf_display = f'''
    #    <iframe src="data:application/pdf;base64,{base64_pdf}#page=3" 
    #            style="width: 70%; height: 900px;" frameborder="0">
    #    </iframe>
    #    '''

    #pdf_display = f'''
    #<div style="display: flex; justify-content: center;">
    #    <iframe src="data:application/pdf;base64,{base64_pdf}#page=3" 
    #            style="width: 70%; height: 900px;" frameborder="0">
    #    </iframe>
    #</div>
    #'''




def get_pdf_base64(file_path):
    with open(file_path, "rb") as f:
        pdf_bytes = f.read()
    return base64.b64encode(pdf_bytes).decode("utf-8")

def open_pdfBase64_works(chunk_id, page):
    # Expected format: Grade08_Science_Chapter13_Chunk06
    parts = chunk_id.split('_')
    if len(parts) < 3:
        print("Invalid chunk_id format")
        return None  # Stop execution if format is wrong
    
    grade, subject, chapter_number = parts[0], parts[1], parts[2]
    print(grade, subject, chapter_number)
    
    if subject.lower() == "science":
        # Use the extracted parts to build the file name
        pdf_filename = f"{grade}_{subject}_{chapter_number}.pdf"
        print("PDF filename:", pdf_filename)
        
        # Get the absolute path to the __pdf folder and the PDF file
        pdf_folder = os.path.abspath('__pdf')
        pdf_path = os.path.join(pdf_folder, pdf_filename)
        print("PDF path:", pdf_path)
    else:
        print("Unsupported subject")
        return None
    
    try:
        base64_pdf = get_pdf_base64(pdf_path)
    except FileNotFoundError:
        print("PDF file not found:", pdf_path)
        return None
    
    #page = 3  # Example page number
    pdf_display = f'''
    <div style="display: flex; justify-content: center; width: 100%;">
        <iframe src="data:application/pdf;base64,{base64_pdf}#page={page}" 
                style="width: 70%; height: 1200px;" frameborder="0">
        </iframe>
    </div>
    '''
    #return pdf_display
    st.markdown(pdf_display, unsafe_allow_html=True)


import os

def open_pdfBase64(chunk_id, page):
    parts = chunk_id.split('_')
    if len(parts) < 3:
        print("Invalid chunk_id format")
        return None  
    
    grade, subject, chapter_number = parts[0], parts[1], parts[2]
    
    if subject.lower() == "science":
        pdf_filename = f"{grade}_{subject}_{chapter_number}.pdf"
        pdf_folder = "__pdf"
        pdf_path = os.path.join(pdf_folder, pdf_filename)
        
        print("Checking PDF path:", pdf_path)
        if not os.path.exists(pdf_path):
            print("Error: PDF file not found at", pdf_path)
            return None
        
        try:
            with open(pdf_path, "rb") as f:
                print("File successfully opened")
                
            base64_pdf = get_pdf_base64(pdf_path)
            pdf_display = f'''
            <div style="display: flex; justify-content: center; width: 100%;">
                <iframe src="data:application/pdf;base64,{base64_pdf}#page={page}" 
                        style="width: 70%; height: 1200px;" frameborder="0">
                </iframe>
            </div>
            '''
            #return pdf_display
            st.markdown(pdf_display, unsafe_allow_html=True)
            return base64_pdf
        
        except Exception as e:
            print("Error converting PDF to Base64:", str(e))
            return None
    else:
        print("Unsupported subject")
        return None



#open_pdfViewer("Grade08_Science_Chapter13-compressed.pdf")

#13,11,10,8,2,1
#pen_pdfBase64_hf('Grade08_Science_Chapter13_Chunk02',2)
