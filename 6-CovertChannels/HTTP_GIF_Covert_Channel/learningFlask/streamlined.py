from flask import Flask, redirect, url_for, request, render_template,send_from_directory, current_app, send_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/picOfTheDay/<name>/<img>', methods=['POST', 'GET'])
def picOfTheDay(name,img):
    uploads = os.path.join(current_app.root_path,app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads,img,as_attachment=True)

@app.route("/",methods = ['POST', 'GET'])
def base():
    if request.method == 'POST':
        user = request.form['nm']
        pic = request.files['img']
        picName = pic.filename
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'],picName))
        return redirect(url_for('picOfTheDay',name=user,img=picName))

    else:
        user = request.args.get('nm')
        pic = request.args.get('img')
        return render_template("picNsource.html",name=user,img=pic)

if __name__ == "__main__":
    app.run(debug = True)
    
