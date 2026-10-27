from app import app
from extensions import db
from models.user import User

def test_login_with_wrong_password_fails():
    client=app.test_client()
    response=client.post("/login", json={"email":"a@b.com", "password":"wrong"})
    assort=response.status_code==401
def test_login_with_correct_password_succeeds():
    with app.app_context():
        user=User(username="testuser",email="login_test@example.com")
        user.set_password("Test12345")
        db.session.add(user)
        db.session.commit()
    client=app.test_client()
    response=client.post("login",json={
        "email":"login_test@example.com",
        "password":"Test12345"
    })
    assert response.status_code==200
    assert "token" in response.get_json()

def test_login_with_missing_password_fails():
    client=app.test_client()
    response=client.post("login",json={"email":"login_test@example.com"})
    assert response.status_code==400
