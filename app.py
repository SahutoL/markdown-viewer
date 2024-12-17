import os, bleach, markdown, uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'md', 'markdown', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_folder():
    session_id = session.get('id')
    if not session_id:
        session_id = str(uuid.uuid4())
        session['id'] = session_id
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)
    return user_folder

@app.route('/')
def index():
    user_folder = get_user_folder()
    files = [f for f in os.listdir(user_folder) if allowed_file(f)]
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = file.filename
        ext = filename.rsplit('.', 1)[1].lower()
        if ext == 'txt':
            filename = filename.rsplit('.', 1)[0] + '.md'
        user_folder = get_user_folder()
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)
    return redirect(url_for('index'))

@app.route('/view/<filename>')
def view_file(filename):
    if not allowed_file(filename):
        return redirect(url_for('index'))
    user_folder = get_user_folder()
    file_path = os.path.join(user_folder, filename)
    if not os.path.exists(file_path):
        return redirect(url_for('index'))
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    html_content = markdown.markdown(
        content,
        extensions=['fenced_code', 'codehilite', 'nl2br'],
        output_format='html5'
    )
    safe_html = bleach.clean(
        html_content,
        tags=['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li', 'code', 'pre', 'strong', 'em', 'hr', 'br']
    )
    return render_template('viewer.html', content=safe_html, filename=filename)

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

if __name__ == '__main__':
    app.run(debug=False)