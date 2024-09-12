import streamlit as st
import PyPDF2
import os
import zipfile
from io import BytesIO

# Title of the app
st.title("PDF Page Extractor - Folder of Individual Pages")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Function to save all pages as separate PDFs in memory and zip them
def save_pages_as_zip(pdf_reader, total_pages):
    # Create an in-memory zip file
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for page_num in range(total_pages):
            # Create a PdfWriter object for each page
            pdf_writer = PyPDF2.PdfWriter()

            # Add the current page
            pdf_writer.add_page(pdf_reader.pages[page_num])

            # Create a binary buffer for each PDF page
            pdf_page_buffer = BytesIO()
            pdf_writer.write(pdf_page_buffer)

            # Write the page to the zip file with a unique name
            pdf_page_name = f"page_{page_num + 1}.pdf"
            zip_file.writestr(pdf_page_name, pdf_page_buffer.getvalue())
    
    # Reset the buffer position to the beginning
    zip_buffer.seek(0)
    return zip_buffer

if uploaded_file is not None:
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    total_pages = len(pdf_reader.pages)

    st.write(f"The PDF has {total_pages} pages.")

    # Button to extract and save all pages as a zip file
    if st.button("Extract and Save All Pages as a ZIP Folder"):
        zip_buffer = save_pages_as_zip(pdf_reader, total_pages)

        # Provide a download button for the zip file
        st.download_button(
            label="Download ZIP Folder",
            data=zip_buffer,
            file_name="pdf_pages.zip",
            mime="application/zip"
        )
