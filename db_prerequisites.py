import os
import time
from flask import Flask
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from models import db

app = Flask(__name__)
database_url = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def create_sql_functions_and_tables():
    # SQL functions
    direction_function = """
    CREATE OR REPLACE FUNCTION direction(
        ax FLOAT, ay FLOAT, bx FLOAT, by FLOAT, cx FLOAT, cy FLOAT
    ) RETURNS FLOAT AS $$
    BEGIN
        RETURN (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
    END;
    $$ LANGUAGE plpgsql;
    """

    on_segment_function = """
    CREATE OR REPLACE FUNCTION on_segment(
        px FLOAT, py FLOAT, qx FLOAT, qy FLOAT, rx FLOAT, ry FLOAT
    ) RETURNS BOOLEAN AS $$
    BEGIN
        RETURN qx <= GREATEST(px, rx) AND qx >= LEAST(px, rx) AND
               qy <= GREATEST(py, ry) AND qy >= LEAST(py, ry);
    END;
    $$ LANGUAGE plpgsql;
    """

    do_lines_intersect_function = """
    CREATE OR REPLACE FUNCTION do_lines_intersect(
        x1 FLOAT, y1 FLOAT, x2 FLOAT, y2 FLOAT,
        u1 FLOAT, v1 FLOAT, u2 FLOAT, v2 FLOAT
    ) RETURNS BOOLEAN AS $$
    DECLARE
        d1 FLOAT;
        d2 FLOAT;
        d3 FLOAT;
        d4 FLOAT;
    BEGIN
        d1 := direction(u1, v1, u2, v2, x1, y1);
        d2 := direction(u1, v1, u2, v2, x2, y2);
        d3 := direction(x1, y1, x2, y2, u1, v1);
        d4 := direction(x1, y1, x2, y2, u2, v2);

        IF ((d1 > 0 AND d2 < 0) OR (d1 < 0 AND d2 > 0)) AND
           ((d3 > 0 AND d4 < 0) OR (d3 < 0 AND d4 > 0)) THEN
            RETURN TRUE;
        ELSIF d1 = 0 AND on_segment(u1, v1, x1, y1, u2, v2) THEN
            RETURN TRUE;
        ELSIF d2 = 0 AND on_segment(u1, v1, x2, y2, u2, v2) THEN
            RETURN TRUE;
        ELSIF d3 = 0 AND on_segment(x1, y1, u1, v1, x2, y2) THEN
            RETURN TRUE;
        ELSIF d4 = 0 AND on_segment(x1, y1, u2, v2, x2, y2) THEN
            RETURN TRUE;
        ELSE
            RETURN FALSE;
        END IF;
    END;
    $$ LANGUAGE plpgsql;
    """

    # SQL table creation
    create_rectangles_table = """
    CREATE TABLE IF NOT EXISTS rectangles (
        rectangle_id SERIAL PRIMARY KEY,
        x1 FLOAT NOT NULL,
        y1 FLOAT NOT NULL,
        x2 FLOAT NOT NULL,
        y2 FLOAT NOT NULL,
        x3 FLOAT NOT NULL,
        y3 FLOAT NOT NULL,
        x4 FLOAT NOT NULL,
        y4 FLOAT NOT NULL
    );
    """

    # Retry mechanism to ensure database is ready
    retries = 5
    while retries > 0:
        try:
            print(f"Trying to connect to the database at {database_url}")
            with app.app_context():
                with db.engine.begin() as conn:
                    conn.execute(text(direction_function))
                    conn.execute(text(on_segment_function))
                    conn.execute(text(do_lines_intersect_function))
                    conn.execute(text(create_rectangles_table))
                    conn.commit()
                    print("SQL functions and table created successfully!")
                    break
        except OperationalError as e:
            print(f"Database connection failed: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1
            if retries == 0:
                raise e


if __name__ == "__main__":
    create_sql_functions_and_tables()
