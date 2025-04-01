import pytest
from datetime import datetime
from app.main import User, Task
from app.database import db

@pytest.fixture
def new_user(db_session):
    """Cria um usuário de teste único"""
    user = User(username='testuser', password='hashedpassword')
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def new_task(new_user, db_session):
    """Cria uma tarefa associada ao usuário de teste"""
    task = Task(content='Test Task', user_id=new_user.id, date_posted=datetime.utcnow())
    db_session.add(task)
    db_session.commit()
    return task

def test_new_user(new_user):
    assert new_user.username == 'testuser'
    assert new_user.password == 'hashedpassword'
    assert repr(new_user) == "User('testuser')"

def test_new_task(new_task):
    assert new_task.content == 'Test Task'
    print("date_posted:", new_task.date_posted)  # Para depuração
    assert isinstance(new_task.date_posted, datetime)
    assert new_task.user_id is not None
    assert repr(new_task).startswith(f"Task('{new_task.content}', ")

def test_user_task_relationship(new_user, new_task):
    new_user.tasks.append(new_task)
    assert new_task in new_user.tasks
