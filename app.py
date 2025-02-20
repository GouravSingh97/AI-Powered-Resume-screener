from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document

app = Flask(__name__)
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = ''
    for para in doc.paragraphs:
        text += para.text + '\n'
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return 'No file part'
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return 'No selected file'
        if resume_file and allowed_file(resume_file.filename):
            filename = secure_filename(resume_file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)

            if filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(filepath)
            elif filename.endswith('.docx'):
                resume_text = extract_text_from_docx(filepath)
            elif filename.endswith('.txt'):
                resume_text = extract_text_from_txt(filepath)

            return render_template('home.html', resume_text=resume_text)

    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
