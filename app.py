from flask import Flask, render_template, request, send_file
import PyPDF2
from docx2pdf import convert
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key
api_key = "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"
openai.api_key = api_key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_to_pdf():
    # Handle document conversion here
    if 'file' in request.files:
        file = request.files['file']
        if file:
            # Save the uploaded file temporarily
            uploaded_file_path = "uploaded_document." + file.filename.split('.')[-1]
            file.save(uploaded_file_path)

            # Check the file type and convert to PDF if it's not already a PDF
            if uploaded_file_path.lower().endswith(('.doc', '.docx')):
                pdf_filename = uploaded_file_path.replace(".docx", ".pdf")
                convert(uploaded_file_path, pdf_filename)
            elif uploaded_file_path.lower().endswith('.pdf'):
                pdf_filename = uploaded_file_path
            else:
                return "Unsupported file format."

            # Provide a download link for the converted PDF
            return send_file(pdf_filename, as_attachment=True)

@app.route('/summarize', methods=['POST'])
def summarize_text():
    # Handle text summarization here
    text = request.form.get('text')
    if text:
        # Use an AI model or NLP library to summarize the text
        # For this example, we'll use a simple summary
        summary = text[:100] if len(text) > 100 else text
        return summary

if __name__ == '__main__':
    app.run(debug=True)
