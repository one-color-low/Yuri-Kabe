from flask import Flask, request, render_template
import zipfile, os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/var/www"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        room_name = request.form['room_name']
        file = request.files['zip_input']
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], room_name)

        with zipfile.ZipFile(file) as existing_zip:
            existing_zip.extractall(path=upload_path)

    return "ok"

@app.route('/upload_page', methods=['GET', 'POST'])
def upload_page():
    return render_template("upload_page.html")


if __name__ == "__main__":
    app.run()