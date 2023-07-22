from flask import Flask, redirect, url_for, request, render_template,send_from_directory, current_app, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route(f'/button_click', methods=['POST','GET'])
def files():
    uploads = os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,"PicofTheDay.jpg",as_attachment=True)

@app.route(f'/picOfTheDay', methods=['POST', 'GET'])
def picOfTheDay():
    if request.method == 'POST':
        user = request.form['nm']
        pic = request.files['img'] 
        upload = request.form['upload']
        download = request.form['btn']
        if not user:
            user = ""
        if pic:
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],"PicofTheDay.jpg"))
            picName = os.path.join(app.config['UPLOAD_FOLDER'],"PicofTheDay.jpg")
        if upload:
            return redirect(url_for('picofTheDay'))
        elif download:
            return redirect(url_for('button_click'))
    else:
        user = request.args.get('nm')
        pic = request.args.get('img')
        return render_template("picNsource.html")

@app.route("/",methods = ['POST', 'GET'])
def base():
    if request.method == 'POST':
        user = request.form['nm']
        if not user:
            user = ""
        pic = request.files['img']
        if pic:
            picName = pic.filename
            pic.save(os.path.join(app.config['UPLOAD_FOLDER'],"PicofTheDay.jpg"))
        return redirect(url_for('picOfTheDay'))
    else:
        user = request.args.get('nm')
        pic = request.args.get('img')
        return render_template("noPic.html")

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug = True)
    
