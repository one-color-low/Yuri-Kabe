from flask import Flask, request, render_template
import zipfile, os
import db_tools

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "/var/www"

#Roomアップロード用API
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        room_id = request.form['room_id']
        file = request.files['zip_input']
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], room_id)

        with zipfile.ZipFile(file) as existing_zip:
            existing_zip.extractall(path=upload_path)
        
        room_url = "http://localhost/store/" + "upload_path" + "/1st"

        return room_url

    else:

        return "ngggggg"

#Room情報保存用API
@app.route('/save_info', methods=['GET', 'POST'])
def save_info():
    if request.method == 'POST':

        if not db_tools.is_exist(request.form['room_id']):

            db_tools.add_entry(
                id = request.form['room_id'],
                author = request.form['author'],
                title = request.form['title'],
                description = request.form['description'],
                tags = request.form['tags']
            )

            return "ok"

        else:

            return "Room Already Exist."

    else:

        return "ng"


# jsonでroom_infoテーブルを上から10個返すAPI
@app.route('/get_list', methods=['GET', 'POST'])
def get_list():
    #table = db_tools.get_latest_n(10)
    #return table
    return "ng"


if __name__ == "__main__":
    app.run()

