import pytest
from flask import Flask
from app.main import db  # Certifique-se de importar o objeto 'db' da sua aplicação
from app.models import User, Task
from datetime import datetime
from app.main import app as flask_app  # Importa a aplicação real


@pytest.fixture(scope="session")
def app():
    """Cria e configura um app Flask para testes"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()  # Cria as tabelas uma vez para a sessão de testes
        yield app
        db.drop_all()  # Remove as tabelas após a sessão de testes

@pytest.fixture(scope="function")
def db_session(app):
    """Cria uma sessão de banco de dados isolada para cada teste usando transações"""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        # Cria uma sessão associada a essa conexão
        options = dict(bind=connection, binds={})
        session = db.create_scoped_session(options=options)
        db.session = session  # Força o uso dessa sessão na aplicação

        yield session  # Aqui o teste é executado

        transaction.rollback()  # Desfaz as alterações realizadas no teste
        connection.close()
        session.remove()

@pytest.fixture(scope="session")
def test_app():
    """Configura a aplicação para os testes"""
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with flask_app.app_context():
        db.create_all()
        yield flask_app
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Cria um cliente de teste usando a fixture test_app"""
    with test_app.test_client() as client:
        with test_app.app_context():
            print(test_app.url_map)  # Exibe todas as rotas registradas
            yield client


@pytest.fixture
def new_task(new_user, db_session):
    """Cria uma tarefa associada ao usuário de teste"""
    task = Task(content='Test Task', user_id=new_user.id, date_posted=datetime.utcnow())
    db_session.add(task)
    db_session.commit()
    return task
