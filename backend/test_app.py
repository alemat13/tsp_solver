import pytest
from flask import Flask
from flask_testing import TestCase
import json

from app import app, get_solver_tour_concorde, get_solver_tour_genetic, get_optimal_route

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_get_solver_tour_concorde(self):
        points = [(1, 1), (2, 2), (3, 3)]
        result = get_solver_tour_concorde(points)
        assert isinstance(result, list)
        assert len(result) == len(points)

    def test_get_solver_tour_genetic(self):
        points = [(1, 1), (2, 2), (3, 3)]
        result = get_solver_tour_genetic(points)
        assert isinstance(result, list)
        assert len(result) == len(points)

    def test_get_optimal_route(self):
        points = [(1, 1), (2, 2), (3, 3)]
        result = get_optimal_route(points)
        assert isinstance(result, list)
        assert len(result) == len(points)

    def test_calculate_route_api(self):
        points = [(1, 1), (2, 2), (3, 3)]
        response = self.client.post('/api/calculate', data=json.dumps(points), content_type='application/json')
        assert response.status_code == 200
        assert isinstance(response.json, list)
        assert len(response.json) == len(points)

    def test_generate_kml(self):
        positions = "1,1\n2,2\n3,3"
        response = self.client.post('/generate_kml', data={'positions': positions})
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/vnd.google-earth.kml+xml'

if __name__ == '__main__':
    pytest.main()