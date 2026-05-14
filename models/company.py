from extensions import db
class Company(db.Model):
    __tablename__="companies"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False,unique=True)
    website=db.Column(db.String(200))
    

    application=db.relationship('JobApplication',backref='company',lazy=True)