import threading

import pytest
from werkzeug.serving import make_server

from app import create_app


@pytest.fixture
def live_server():
    app = create_app()
    server = make_server("127.0.0.1", 0, app)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield f"http://127.0.0.1:{port}"

    server.shutdown()
    thread.join()
