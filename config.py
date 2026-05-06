import os
BASE_DIR=os.path.abspath(os.path.dirname(__file__))
class config:
    SECRET_KEY="dev-secret-key"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "job_tracker.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS=False