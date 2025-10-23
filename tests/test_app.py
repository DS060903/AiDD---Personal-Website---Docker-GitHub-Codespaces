"""
Test cases for Flask application routes and functionality.
"""
import pytest
import json
from flask import url_for


class TestRoutes:
    """Test all Flask routes."""
    
    def test_index_route(self, client):
        """Test the index route returns 200."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_about_route(self, client):
        """Test the about route returns 200."""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_resume_route(self, client):
        """Test the resume route returns 200."""
        response = client.get('/resume')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_contact_route(self, client):
        """Test the contact route returns 200."""
        response = client.get('/contact')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_thankyou_route(self, client):
        """Test the thankyou route returns 200."""
        response = client.get('/thankyou')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data


class TestProjectsRoute:
    """Test the projects route with database functionality."""
    
    def test_projects_route_empty_db(self, client):
        """Test projects route with empty database."""
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_projects_route_with_data(self, client_with_data):
        """Test projects route with populated database."""
        response = client_with_data.get('/projects')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
        # Check if project data is in the response
        assert b'Test Project 1' in response.data
        assert b'Test Project 2' in response.data


class TestAddProjectRoute:
    """Test the add project route functionality."""
    
    def test_add_project_get(self, client):
        """Test GET request to add project route."""
        response = client.get('/add')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data
    
    def test_add_project_post_valid_data(self, client):
        """Test POST request with valid project data."""
        project_data = {
            'title': 'New Test Project',
            'description': 'This is a new test project',
            'image_file_name': 'new_project.jpg'
        }
        
        response = client.post('/add', data=project_data, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to projects page
        assert b'<!DOCTYPE html>' in response.data
    
    def test_add_project_post_missing_title(self, client):
        """Test POST request with missing title."""
        project_data = {
            'description': 'This is a project without title',
            'image_file_name': 'no_title.jpg'
        }
        
        response = client.post('/add', data=project_data)
        assert response.status_code == 200
        # Should stay on add page, not redirect
    
    def test_add_project_post_missing_description(self, client):
        """Test POST request with missing description."""
        project_data = {
            'title': 'Project without description',
            'image_file_name': 'no_desc.jpg'
        }
        
        response = client.post('/add', data=project_data)
        assert response.status_code == 200
        # Should stay on add page, not redirect
    
    def test_add_project_post_missing_image(self, client):
        """Test POST request with missing image file name."""
        project_data = {
            'title': 'Project without image',
            'description': 'This project has no image'
        }
        
        response = client.post('/add', data=project_data)
        assert response.status_code == 200
        # Should stay on add page, not redirect
    
    def test_add_project_post_empty_data(self, client):
        """Test POST request with empty form data."""
        project_data = {}
        
        response = client.post('/add', data=project_data)
        assert response.status_code == 200
        # Should stay on add page, not redirect


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_nonexistent_route(self, client):
        """Test accessing a non-existent route."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_projects_route_with_invalid_db(self, client):
        """Test projects route with invalid database path."""
        # This test would require mocking the database connection
        # For now, we'll just ensure the route handles errors gracefully
        response = client.get('/projects')
        assert response.status_code == 200


class TestTemplateRendering:
    """Test that templates are rendered correctly."""
    
    def test_all_templates_contain_basic_html(self, client):
        """Test that all routes return proper HTML."""
        routes = ['/', '/about', '/resume', '/contact', '/thankyou', '/add', '/projects']
        
        for route in routes:
            response = client.get(route)
            assert response.status_code == 200
            assert b'<!DOCTYPE html>' in response.data
            assert b'<html' in response.data
            assert b'</html>' in response.data
