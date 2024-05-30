import pytest
from models import db, Rectangle
from app import app as flask_app


class TestRectangleAPI:
    @pytest.fixture
    def client(self):
        return flask_app.test_client()

    def test_create_rectangle(self, client):
        response = client.post('/rectangles', json={
            'x1': 1, 'y1': 1,
            'x2': 1, 'y2': 3,
            'x3': 3, 'y3': 3,
            'x4': 3, 'y4': 1
        })
        assert response.status_code == 201
        data = response.get_json()
        assert 'rectangle' in data
        assert 'message' in data

    def test_create_bad_rectangle(self, client):
        response = client.post('/rectangles', json={
            'x1': 0, 'y1': 1,
            'x2': 1, 'y2': 3,
            'x3': 3, 'y3': 3,
            'x4': 3, 'y4': 1
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'message' in data
        assert data['message'] == 'The given points do not form a rectangle!'

    def test_get_rectangles(self, client):
        rectangle = Rectangle(x1=0, y1=0, x2=4, y2=-4, x3=7, y3=-1, x4=3, y4=3)
        with flask_app.app_context():
            db.session.add(rectangle)
            db.session.commit()
            response = client.get('/rectangles')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_rectangle(self, client):
        rectangle = Rectangle(x1=-6, y1=-4, x2=-4, y2=-6, x3=0, y3=-2, x4=-2, y4=0)
        with flask_app.app_context():
            db.session.add(rectangle)
            db.session.commit()
            response = client.get(f'/rectangles/{rectangle.rectangle_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['x1'] == -6

    def test_update_rectangle(self, client):
        rectangle = Rectangle(x1=1, y1=1, x2=1, y2=3, x3=3, y3=3, x4=3, y4=1)
        with flask_app.app_context():
            db.session.add(rectangle)
            db.session.commit()
            response = client.patch(f'/rectangles/{rectangle.rectangle_id}', json={
                'x1': -6, 'y1': -2,
                'x2': -2, 'y2': -6,
                'x3': 3, 'y3': -1,
                'x4': -1, 'y4': 3
            })
            rectangle_id = rectangle.rectangle_id
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Rectangle updated'
        with flask_app.app_context():
            updated_rectangle = Rectangle.query.get(rectangle_id)
            assert updated_rectangle.x1 == -6

    def test_delete_rectangle(self, client):
        rectangle = Rectangle(x1=1, y1=1, x2=1, y2=3, x3=3, y3=3, x4=3, y4=1)
        with flask_app.app_context():
            db.session.add(rectangle)
            db.session.commit()
            response = client.delete(f'/rectangles/{rectangle.rectangle_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Rectangle deleted'
        with flask_app.app_context():
            assert Rectangle.query.get(rectangle.rectangle_id) is None

    def test_intersection(self, client):
        u1 = 2
        v1 = 2
        u2 = 5
        v2 = 3
        rectangle = Rectangle(x1=3, y1=3, x2=6, y2=6, x3=8, y3=4, x4=5, y4=1)
        with flask_app.app_context():
            db.session.add(rectangle)
            db.session.commit()
            response = client.post('/intersecting_rectangles', json={
                "u1": u1, "v1": v1,
                "u2": u2, "v2": v2
            })
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) > 0


if __name__ == "__main__":
    pytest.main()
