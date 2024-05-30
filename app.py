import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from models import db, Rectangle

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
database_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)


@app.route('/intersecting_rectangles', methods=['POST'])
def get_intersecting_rectangles():
    data = request.json
    u1 = data['u1']
    v1 = data['v1']
    u2 = data['u2']
    v2 = data['v2']

    query = text('''
        WITH segment AS (
            SELECT 1 AS id, 
            :u1 AS u1, :v1 AS v1, 
            :u2 AS u2, :v2 AS v2
        ),
        segment_bbox AS (
            SELECT s.id,
            LEAST(s.u1, s.u2) AS min_x,
            GREATEST(s.u1, s.u2) AS max_x,
            LEAST(s.v1, s.v2) AS min_y,
            GREATEST(s.v1, s.v2) AS max_y
            FROM segment s
        ),
        filtered_rectangles AS (
            SELECT r.rectangle_id, r.x1, r.y1, r.x2, r.y2, r.x3, r.y3, r.x4, r.y4
            FROM rectangles r
            CROSS JOIN segment_bbox sb
            WHERE 
            (LEAST(r.x1, r.x2, r.x3, r.x4) <= sb.max_x AND
            GREATEST(r.x1, r.x2, r.x3, r.x4) >= sb.min_x) AND
            (LEAST(r.y1, r.y2, r.y3, r.y4) <= sb.max_y AND
            GREATEST(r.y1, r.y2, r.y3, r.y4) >= sb.min_y)
        )
        SELECT DISTINCT r.rectangle_id, r.x1, r.y1, r.x2, r.y2, r.x3, r.y3, r.x4, r.y4
        FROM rectangles r
        JOIN filtered_rectangles fr ON r.rectangle_id = fr.rectangle_id
        JOIN segment s ON 1 = 1
        WHERE (
        (do_lines_intersect(r.x1, r.y1, r.x2, r.y2, s.u1, s.v1, s.u2, s.v2)) OR
        (do_lines_intersect(r.x2, r.y2, r.x3, r.y3, s.u1, s.v1, s.u2, s.v2)) OR
        (do_lines_intersect(r.x3, r.y3, r.x4, r.y4, s.u1, s.v1, s.u2, s.v2)) OR
        (do_lines_intersect(r.x4, r.y4, r.x1, r.y1, s.u1, s.v1, s.u2, s.v2))
        );
    ''')

    result = db.session.execute(query, {'u1': u1, 'v1': v1, 'u2': u2, 'v2': v2})
    rectangles = [
        {'rectangle_id': row[0], 'x1': row[1], 'y1': row[2], 'x2': row[3], 'y2': row[4], 'x3': row[5], 'y3': row[6],
         'x4': row[7], 'y4': row[8]} for row in result]

    return jsonify({'intersecting_rectangles': rectangles})


@app.route('/rectangles', methods=['POST'])
def create_rectangle():
    data = request.get_json()
    new_rectangle = Rectangle(
        x1=data['x1'],
        y1=data['y1'],
        x2=data['x2'],
        y2=data['y2'],
        x3=data['x3'],
        y3=data['y3'],
        x4=data['x4'],
        y4=data['y4']
    )
    db.session.add(new_rectangle)
    db.session.commit()
    return jsonify({'message': 'Rectangle created', 'rectangle': new_rectangle.rectangle_id}), 201


@app.route('/rectangles', methods=['GET'])
def get_rectangles():
    rectangles = Rectangle.query.all()
    return jsonify([{
        'rectangle_id': rect.rectangle_id,
        'x1': rect.x1,
        'y1': rect.y1,
        'x2': rect.x2,
        'y2': rect.y2,
        'x3': rect.x3,
        'y3': rect.y3,
        'x4': rect.x4,
        'y4': rect.y4
    } for rect in rectangles])


@app.route('/rectangles/<int:rectangle_id>', methods=['GET'])
def get_rectangle(rectangle_id):
    rectangle = Rectangle.query.get_or_404(id)
    return jsonify({
        'rectangle_id': rectangle.rectangle_id,
        'x1': rectangle.x1,
        'y1': rectangle.y1,
        'x2': rectangle.x2,
        'y2': rectangle.y2,
        'x3': rectangle.x3,
        'y3': rectangle.y3,
        'x4': rectangle.x4,
        'y4': rectangle.y4
    })


@app.route('/rectangles/<int:rectangle_id>', methods=['PUT'])
def update_rectangle(rectangle_id):
    rectangle = Rectangle.query.get_or_404(rectangle_id)
    data = request.get_json()
    rectangle.x1 = data['x1']
    rectangle.y1 = data['y1']
    rectangle.x2 = data['x2']
    rectangle.y2 = data['y2']
    rectangle.x3 = data['x3']
    rectangle.y3 = data['y3']
    rectangle.x4 = data['x4']
    rectangle.y4 = data['y4']
    db.session.commit()
    return jsonify({'message': 'Rectangle updated'})


@app.route('/rectangles/<int:rectangle_id>', methods=['DELETE'])
def delete_rectangle(rectangle_id):
    rectangle = Rectangle.query.get_or_404(rectangle_id)
    db.session.delete(rectangle)
    db.session.commit()
    return jsonify({'message': 'Rectangle deleted'})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(host='0.0.0.0')
