import pytest


def test_api_get_types(client, app, test_db):
    with app.app_context():
        response = client.get('/api/types?typology=Temporistics')
        assert response.status_code == 200
        data = response.get_json()
        assert 'types' in data
        assert any('Past' in t for t in data['types'])


def test_api_calculate(client, app, test_db):
    with app.app_context():
        payload = {
            'user1': 'Past, Current, Future, Eternity',
            'user2': 'Past, Current, Future, Eternity',
            'typology': 'Temporistics'
        }
        response = client.post('/api/calculate', json=payload)
        assert response.status_code == 200
        data = response.get_json()
        assert 'relationship_type' in data
        assert 'comfort_score' in data


def test_api_calculate_missing_params(client, app, test_db):
    with app.app_context():
        response = client.post('/api/calculate', json={'user1': 'A'})
        assert response.status_code == 400

