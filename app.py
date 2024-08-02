import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import markdown
import bleach

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

ALLOWED_EXTENSIONS = {'md', 'markdown'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if allowed_file(f)]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    if not allowed_file(filename):
        return redirect(url_for('index'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown.markdown(content, extensions=['fenced_code', 'codehilite'])
    safe_html = bleach.clean(html_content, tags=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li', 'code', 'pre', 'strong', 'em'])
    return render_template('viewer.html', content=safe_html, filename=filename)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT')))