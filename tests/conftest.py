import pytest
from app import create_app
from app import models


@pytest.fixture
def test_db(tmp_path):
    """Fixture para tests de models.py"""
    db_path = tmp_path / "test.db"
    if db_path.exists():
        db_path.unlink()
    models.init_db(db_path)
    return db_path


@pytest.fixture
def app(tmp_path):
    """Crea una aplicación Flask configurada para testing"""
    db_path = tmp_path / "test_api.db"

    original_db = models.DEFAULT_DATABASE
    models.DEFAULT_DATABASE = db_path

    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        models.init_db()

    yield app

    models.DEFAULT_DATABASE = original_db


@pytest.fixture
def client(app):
    """Crea un cliente de test para hacer peticiones HTTP"""
    return app.test_client()


@pytest.fixture(autouse=True, scope="function")
def clear_db(app):
    """
    Limpia la base de datos antes de cada test.
    autouse=True hace que se ejecute automáticamente.
    """
    # Ejecutar antes del test
    with app.app_context():
        models.clear_tasks()

    yield  # El test se ejecuta aquí
