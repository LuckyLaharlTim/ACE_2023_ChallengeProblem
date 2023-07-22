from flask import Flask, redirect, url_for, request, render_template,send_from_directory, current_app, send_file
import os
import socket

app = Flask(__name__)
UPLOAD_FOLDER = 'files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route(f'/button_click', methods=['POST','GET'])
def files():
    uploads = os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,"PicofTheDay.png",as_attachment=True)

@app.route(f'/picOfTheDay', methods=['POST', 'GET'])
def picOfTheDay():
    if request.method == 'POST':
        button = request.form['btn']
        return redirect(url_for('button_click'))
    else:
        user = request.args.get('nm')
        pic = request.args.get('img')
        return render_template("picNsourceOnly.html")

@app.route("/upload",methods = ['POST', 'GET'])
def base():
    if request.method == 'POST':
        pic = request.files['img']
        if pic:
            picType = pic.filename.split(".")[-1]
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],"PicofTheDay.png"))
        return redirect(url_for('picOfTheDay'))
    else:
        user = request.args.get('nm')
        pic = request.args.get('img')
        return render_template("newPic.html")

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="192.168.12.61",port=5000,debug = True)
    
    
