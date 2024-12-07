import pytest

def test_404_error(client):
    response = client.get("/this_route_does_not_exist")
    assert response.status_code == 404
    assert b"404" in response.data

def test_500_error(client):
    # Теперь маршрут уже определён в app/__init__.py при TESTING=True
    # Просто вызываем его
    response = client.get("/cause_500")
    assert response.status_code == 500
    assert b"500" in response.data
