from app import create_app


def make_client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_patch_toggles_completed_false_to_true():
    client = make_client()

    response = client.patch("/todos/1", json={"completed": True})

    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "title": "Buy milk", "completed": True}


def test_patch_toggles_completed_true_to_false():
    client = make_client()
    client.patch("/todos/1", json={"completed": True})

    response = client.patch("/todos/1", json={"completed": False})

    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "title": "Buy milk", "completed": False}


def test_patch_nonexistent_id_returns_404():
    client = make_client()

    response = client.patch("/todos/999", json={"completed": True})

    assert response.status_code == 404


def test_patch_missing_completed_key_returns_400():
    client = make_client()

    response = client.patch("/todos/1", json={})

    assert response.status_code == 400
