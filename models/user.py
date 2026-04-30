from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(200),nullable=False)

    application=db.relationship('JobApplication',backref='user',lazy=True)

    def set_password(self,raw_password):
        self.password=generate_password_hash(raw_password)
    
    def check_password(self,raw_password):
        return check_password_hash(self.password,raw_password)
def __repr__(self):
        return f"<User {self.email}>"   