from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os, os.path

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/get_status")
def get_status():
    return jsonify(status_code=200,
                   db_size=len([name for name in os.listdir(app.config['UPLOAD_FOLDER'])
                           if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], name))]))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file'
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'stored'
        return 'File error'


if __name__ == '__main__':
    # To start flask application, run:
    # flask run --host=0.0.0.0 -p 5000
    app.run(host='0.0.0.0', debug=True)