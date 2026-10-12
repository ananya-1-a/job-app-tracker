from app import app

def test_login_with_wrong_password_fails():
    client=app.test_client()
    response=client.post("/login", json={"email":"a@b.com", "password":"wrong"})
    assort=response.status_code==401