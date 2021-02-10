from db import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    labelled = db.Column(db.Boolean, nullable=True)
    
class Labels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
class ImgLbl(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('img.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    isPresent = db.Column(db.Boolean)
    image = db.relationship(Img, backref=db.backref("img", cascade="all, delete-orphan"))
    labels = db.relationship(Labels, backref=db.backref("Labels", cascade="all, delete-orphan"))

    
    
# image_labels = db.Table(
    # "image_labels",
    # db.Column("image_id", db.Integer, db.ForeignKey("img.id")),
    # db.Column("label_id", db.Integer, db.ForeignKey("labels.id")),
    # db.Column("isPresent", db.Boolean)
# )
