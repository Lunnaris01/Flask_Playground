import pandas as pd
from flask import Flask, request, make_response, render_template, redirect, url_for, Response, send_from_directory,jsonify
import datetime
import os
import uuid
import pandas

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', year=datetime.datetime.now().year, foottext="This is the foottext")

@app.route('/index_post',methods = ['GET', 'POST'])
def index_post():
    if request.method == 'GET':
        return render_template('index_post.html', year=datetime.datetime.now().year, foottext="Foottext for the Post Requests Page")
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == 'password':
            return render_template('member_landing_page.html', username="admin")
        else:
            return render_template('index_post_wrongpass.html', year=datetime.datetime.now().year,foottext="Wrong username or password")


@app.route('/member_landing_page')
def member_landing_page(username):
    return render_template('member_landing_page.html', username="admin")

@app.route('/index_2')
def index2():
    today = datetime.datetime.now()
    return render_template('index_2.html', year=datetime.datetime.now().year, date=[today.day, today.month, today.year])


@app.route('/redirect_endpoint')
def redirect_endpoint():
    return redirect(url_for('index'))

@app.route('/file_upload',methods = ['GET', 'POST'])
def file_upload():
    file = request.files.get('file')

    if file.content_type == 'text/plain':
        return file.read().decode()
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or file.content_type == 'application/vnd.ms-excel':
        df = pd.read_excel(file)
        return df.to_html()
    else:
        return ""

@app.route('/convert_csv',methods = ['GET', 'POST'])
def convert_csv():
    if request.method == 'POST':
        file = request.files.get('file')

        exel_file = pd.read_excel(file)
        response = Response(
            exel_file.to_csv(),
            mimetype='text/csv',
            headers ={
                'Content-Disposition': 'attachment; filename=result.csv'
            }
        )
        return response

@app.route("/convert_csv_downloadpage",methods = ['GET', 'POST'])
def convert_csv_downloadpage():
    file = request.files.get('file')
    exel_file = pd.read_excel(file)


    os.makedirs("../downloads", exist_ok=True)
    filename = f'{uuid.uuid4()}.csv'

    exel_file.to_csv(os.path.join('../downloads', filename))
    return render_template("memberpage_download.html", filename=filename)

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory("../downloads", filename, download_name="result.csv")


@app.route("/handle_post_json",methods = ['POST'])
def handle_post_json():
    greeting = request.json.get('greeting')
    name = request.json.get('name')
    with open('../file.txt', 'w') as f:
        f.write(f'{greeting}, {name}')

    return jsonify({'message': 'Successfully written file.'})

@app.route("/hello", methods=['GET', 'POST'])
def hello():
    if request.method == 'GET':
        response = make_response("Hello to your GET request!\n")
        response.status_code = 202
        response.headers['Content-Type'] = 'text/plain'
        return response
    elif request.method == 'POST':
        return "We say Hello to your POST request\n", 202


@app.template_filter('reverse_string')
def reverse_string(s):
    return s[::-1]


@app.template_filter('slice')
def slice(s, start, end):
    return s[start:end]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
