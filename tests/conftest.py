"""
Pytest configuration and fixtures for Flask application testing.
"""
import pytest
import tempfile
import os
from flask import Flask
import sys
import os

# Add the parent directory to the path so we can import app and DAL
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from DAL import init_db, get_all_projects, insert_project


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary file to serve as the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    flask_app.config.update({
        'TESTING': True,
        'DATABASE': db_path
    })
    
    # Initialize the database
    init_db(db_path)
    
    # Monkey patch the DAL functions to use the test database
    import DAL
    original_init_db = DAL.init_db
    original_get_all_projects = DAL.get_all_projects
    original_insert_project = DAL.insert_project
    
    DAL.init_db = lambda db_path_param="projects.db": init_db(db_path)
    DAL.get_all_projects = lambda db_path_param="projects.db": get_all_projects(db_path)
    DAL.insert_project = lambda title, description, image_file_name, db_path_param="projects.db": insert_project(title, description, image_file_name, db_path)
    
    yield flask_app
    
    # Restore original functions
    DAL.init_db = original_init_db
    DAL.get_all_projects = original_get_all_projects
    DAL.insert_project = original_insert_project
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


@pytest.fixture
def sample_projects():
    """Sample project data for testing."""
    return [
        {
            'title': 'Test Project 1',
            'description': 'This is a test project description',
            'image_file_name': 'test1.jpg'
        },
        {
            'title': 'Test Project 2', 
            'description': 'Another test project description',
            'image_file_name': 'test2.jpg'
        }
    ]


@pytest.fixture
def populated_db(app, sample_projects):
    """Create a database with sample projects."""
    db_path = app.config['DATABASE']
    
    # Insert sample projects
    for project in sample_projects:
        insert_project(
            project['title'],
            project['description'], 
            project['image_file_name'],
            db_path
        )
    
    return db_path


@pytest.fixture
def client_with_data(client, populated_db):
    """A test client with populated database."""
    return client
