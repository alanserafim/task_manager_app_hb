# import pytest
# from flask_login import login_user
# from app.main import User, Task, bcrypt
# from datetime import datetime

# @pytest.fixture
# def new_user(db_session):
#     """Cria um usuário de teste com senha hasheada"""
#     hashed_password = bcrypt.generate_password_hash("testpassword").decode('utf-8')
#     user = User(username='testuser', password=hashed_password)
#     db_session.add(user)
#     db_session.commit()
#     return user


# def test_register(client, db_session):
#     # Testa registro com dados válidos
#     response = client.post("/register", 
#         data={
#             "username": "newuser",
#             "password": "validpassword123",
#             "confirm_password": "validpassword123"
#         },
#         follow_redirects=True
#     )
#     assert response.status_code == 200
    
#     # Verifica se o usuário foi criado no banco
#     user = User.query.filter_by(username="newuser").first()
#     assert user is not None


# def test_login(client, new_user):
#     response = client.post("/login", data={
#         "username": new_user.username,
#         "password": "hashedpassword"
#     }, follow_redirects=True)
#     assert b"Login Successfull" in response.data

# def test_logout(client):
#     response = client.get("/logout", follow_redirects=True)
#     assert b"Login" in response.data

# def test_add_task(client, new_user, db_session):
#     login_user(new_user)
#     response = client.post("/add_task", data={"task_name": "New Task"}, follow_redirects=True)
#     assert b"Task Created" in response.data

# def test_update_task(client, new_user, new_task, db_session):
#     login_user(new_user)
#     response = client.post(f"/all_tasks/{new_task.id}/update_task", data={"task_name": "Updated Task"}, follow_redirects=True)
#     assert b"Task Updated" in response.data

# def test_delete_task(client, new_user, new_task, db_session):
#     login_user(new_user)
#     response = client.get(f"/all_tasks/{new_task.id}/delete_task", follow_redirects=True)
#     assert b"Task Deleted" in response.data
