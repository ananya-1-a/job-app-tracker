from extensions import db
from datetime import datetime

class JobApplication(db.Model):
    __tablename__ = "job_applications"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    role = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default="Applied")
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    current_round=db.Column(db.String(100),nullable=True,default='Initial Application')
    # I REMOVED THE TWO db.relationship LINES FROM HERE. 
    # user.py file is already handling this automatically!

    def __repr__(self):
        return f"<JobApplication {self.role} at {self.company_id}>"