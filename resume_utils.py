import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from all pages of an uploaded PDF file.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text from the PDF.
             Returns an empty string if extraction fails.
    """

    # Return empty string if no file is uploaded
    if uploaded_file is None:
        return ""

    try:
        # Read the uploaded PDF as bytes
        pdf_bytes = uploaded_file.read()

        # Open the PDF from bytes
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

        # Variable to store extracted text
        extracted_text = ""

        # Loop through every page in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)

            # Extract text from the current page
            extracted_text += page.get_text()

            # Add a newline between pages
            extracted_text += "\n"

        # Close the document after extraction
        pdf_document.close()

        return extracted_text

    except Exception as e:
        # Print the error for debugging
        print(f"Error extracting PDF text: {e}")

        # Return an empty string if an error occurs
        return ""
    
