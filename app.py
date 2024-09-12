import streamlit as st
import PyPDF2

# Title of the app
st.title("PDF Page Extractor")

# Upload PDF file
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    total_pages = len(pdf_reader.pages)

    st.write(f"The PDF has {total_pages} pages.")
    
    # Select which page to display or extract
    selected_page = st.number_input("Select page to extract or view", min_value=1, max_value=total_pages, value=1)

    # Button to extract and display the selected page
    if st.button("Extract and Display Page"):
        page = pdf_reader.pages[selected_page - 1]
        page_text = page.extract_text()
        st.write(f"Page {selected_page} Content:")
        st.text(page_text)
    
    # Option to save the selected page as a separate PDF
    if st.button("Save Page as PDF"):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[selected_page - 1])
        
        output_filename = f"page_{selected_page}.pdf"
        
        # Create a binary buffer to hold the new PDF data
        with open(output_filename, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

        st.success(f"Page {selected_page} has been saved as {output_filename}.")
        with open(output_filename, "rb") as file:
            btn = st.download_button(
                label="Download Page PDF",
                data=file,
                file_name=output_filename,
                mime="application/octet-stream"
            )

