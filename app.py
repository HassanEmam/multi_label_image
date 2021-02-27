from flask import Flask, request, Response, render_template, send_from_directory, redirect,url_for
from werkzeug.utils import secure_filename
import os

from db import db_init, db
from models import Img, Labels, ImgLbl

app = Flask(__name__)
# SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)
APP_ROOT = os.path.dirname(__file__)


@app.route('/')
def hello_world():

    img = Img.query.filter_by(labelled=False).first()
    if img:
        imsrc= 'images/' + img.name
        labels = Labels.query.all()
        return render_template('labels.html', labels=labels, img=img, imsrc=imsrc)
    return "No Images Found"

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        pic = request.files['pic']
        if not pic:
            return 'No pic uploaded!', 400
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            return 'Bad upload!', 400

        img = Img(img=pic.read(), name=filename, mimetype=mimetype)
        db.session.add(img)
        db.session.commit()
        return 'Img Uploaded!', 200
    return render_template('index.html')

@app.route('/labels', methods=['GET', 'POST'])
def labels():
    if request.method == "GET":
        img = Img.query.filter_by(labelled=False).first()
        if img:
            imsrc= 'images/' + img.name
            labels = Labels.query.all()
            return render_template('labels.html', labels=labels, img=img, imsrc=imsrc)
        return "No Images Found"
    else:
        return "POST"

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        img_id = request.form.get('imgId')
        imageObj = Img.query.filter_by(id=img_id).first()
        lbls = request.form.getlist('labels')
        for l in lbls:
            imglbl = ImgLbl(image_id= img_id, label_id=l, isPresent=True)
            db.session.add(imglbl)
        imageObj.labelled= True
        db.session.commit()
        return redirect(url_for('labels'))

@app.route('/getimage/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)
    
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      files = request.files.getlist("file")
      for file in files:
          filename = secure_filename(file.filename)
          mimetype = file.mimetype
          file.save(os.path.join(os.path.join(APP_ROOT, 'images'), filename))
          img = Img(name=filename, mimetype=mimetype, labelled= False)
          db.session.add(img)
          db.session.commit()
          
      return 'file uploaded successfully'

if __name__ == '__main__':
   app.run(debug = True)



@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)
