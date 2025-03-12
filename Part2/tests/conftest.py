# Part2/tests/conftest.py
import pytest
from app import create_app, db

@pytest.fixture(scope="module")
def test_client():
    app = create_app(testing=True)
    testing_client = app.test_client()
    
    with app.app_context():
        db.create_all()
        yield testing_client
        db.session.remove()
        db.drop_all()