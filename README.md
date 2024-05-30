# Flask Rectangle API

This project is a Flask-based API for managing rectangles and determining their intersection with a given segment. The application uses SQLAlchemy for ORM and supports basic CRUD operations for rectangles.

## Features

- Create, read, update, and delete rectangles.
- Check which rectangles intersect with a given segment.

## Requirements

- Python 3.8+
- Flask
- Flask-SQLAlchemy
- psycopg2-binary
- SQLAlchemy
- pytest

## Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/rectangle-api.git
cd rectangle-api
```

### Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

First, create the database and tables:

```bash
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
```

Run the Flask application:

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Create a Rectangle

**POST /rectangles**

```json
{
    "x1": 1.0,
    "y1": 1.0,
    "x2": 1.0,
    "y2": 3.0,
    "x3": 3.0,
    "y3": 3.0,
    "x4": 3.0,
    "y4": 1.0
}
```

### Get All Rectangles

**GET /rectangles**

### Get a Single Rectangle

**GET /rectangles/<id>**

### Update a Rectangle

**PUT /rectangles/<id>**

```json
{
    "x1": 2.0,
    "y1": 2.0,
    "x2": 2.0,
    "y2": 4.0,
    "x3": 4.0,
    "y3": 4.0,
    "x4": 4.0,
    "y4": 2.0
}
```

### Delete a Rectangle

**DELETE /rectangles/<id>**

### Check Intersections

**GET /rectangles/intersect**

```json
{
    "u1": 0,
    "v1": 2,
    "u2": 5,
    "v2": 2
}
```

## Running Tests

To run the tests, ensure you have `pytest` installed:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_app.py
```

## Docker Setup

You can run the application using Docker. Here’s how:

### Dockerfile

```dockerfile
# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_APP: app.py
      FLASK_RUN_HOST: 0.0.0.0
      FLASK_ENV: development
```

### Build and Run with Docker

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`.