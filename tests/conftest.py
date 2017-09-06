import pytest
from flask import Flask


@pytest.fixture
def app():

    test_app = Flask(__name__)

    @test_app.route('/')
    def index():
        return '<h1>Hello World!</h1>'

    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(request, app):

    client = app.test_client()

    def teardown():
        pass
    request.addfinalizer(teardown)

    return client
