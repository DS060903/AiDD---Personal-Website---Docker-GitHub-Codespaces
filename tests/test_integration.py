"""
Integration tests for the complete Flask application workflow.
"""
import pytest
import json


class TestCompleteWorkflow:
    """Test complete user workflows."""
    
    def test_add_project_and_view_workflow(self, client):
        """Test complete workflow: add project -> view projects."""
        # Step 1: Access the add project page
        response = client.get('/add')
        assert response.status_code == 200
        
        # Step 2: Add a new project
        project_data = {
            'title': 'Integration Test Project',
            'description': 'This is a test project for integration testing',
            'image_file_name': 'integration_test.jpg'
        }
        
        response = client.post('/add', data=project_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Step 3: View the projects page to verify the project was added
        response = client.get('/projects')
        assert response.status_code == 200
        assert b'Integration Test Project' in response.data
        assert b'This is a test project for integration testing' in response.data
    
    def test_multiple_projects_workflow(self, client):
        """Test adding multiple projects and viewing them."""
        projects_data = [
            {
                'title': 'Project Alpha',
                'description': 'First project description',
                'image_file_name': 'alpha.jpg'
            },
            {
                'title': 'Project Beta', 
                'description': 'Second project description',
                'image_file_name': 'beta.jpg'
            },
            {
                'title': 'Project Gamma',
                'description': 'Third project description', 
                'image_file_name': 'gamma.jpg'
            }
        ]
        
        # Add all projects
        for project_data in projects_data:
            response = client.post('/add', data=project_data, follow_redirects=True)
            assert response.status_code == 200
        
        # View projects page
        response = client.get('/projects')
        assert response.status_code == 200
        
        # Verify all projects are displayed
        for project_data in projects_data:
            assert project_data['title'].encode() in response.data
            assert project_data['description'].encode() in response.data
    
    def test_navigation_workflow(self, client):
        """Test complete navigation through all pages."""
        pages = ['/', '/about', '/resume', '/contact', '/projects', '/add', '/thankyou']
        
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200
            assert b'<!DOCTYPE html>' in response.data


class TestFormValidation:
    """Test form validation and error handling."""
    
    def test_add_project_form_validation(self, client):
        """Test form validation for add project."""
        # Test with missing title
        response = client.post('/add', data={
            'description': 'Test description',
            'image_file_name': 'test.jpg'
        })
        assert response.status_code == 200
        # Should stay on add page (not redirect)
        
        # Test with missing description
        response = client.post('/add', data={
            'title': 'Test title',
            'image_file_name': 'test.jpg'
        })
        assert response.status_code == 200
        
        # Test with missing image
        response = client.post('/add', data={
            'title': 'Test title',
            'description': 'Test description'
        })
        assert response.status_code == 200
        
        # Test with all fields present
        response = client.post('/add', data={
            'title': 'Valid Project',
            'description': 'Valid description',
            'image_file_name': 'valid.jpg'
        }, follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to projects page


class TestDataPersistence:
    """Test that data persists across requests."""
    
    def test_data_persistence_across_requests(self, client):
        """Test that added projects persist across multiple requests."""
        # Add a project
        project_data = {
            'title': 'Persistent Project',
            'description': 'This project should persist',
            'image_file_name': 'persistent.jpg'
        }
        
        response = client.post('/add', data=project_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Make multiple requests to projects page
        for _ in range(3):
            response = client.get('/projects')
            assert response.status_code == 200
            assert b'Persistent Project' in response.data
            assert b'This project should persist' in response.data
    
    def test_multiple_sessions_data_isolation(self, client):
        """Test that data is properly isolated between different test sessions."""
        # This test ensures that each test gets a clean database
        response = client.get('/projects')
        assert response.status_code == 200
        
        # Add a project
        project_data = {
            'title': 'Session Test Project',
            'description': 'Session test description',
            'image_file_name': 'session.jpg'
        }
        
        response = client.post('/add', data=project_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify project exists
        response = client.get('/projects')
        assert b'Session Test Project' in response.data


class TestErrorRecovery:
    """Test application error recovery and resilience."""
    
    def test_invalid_route_handling(self, client):
        """Test handling of invalid routes."""
        invalid_routes = ['/invalid', '/nonexistent', '/admin', '/api/test']
        
        for route in invalid_routes:
            response = client.get(route)
            assert response.status_code == 404
    
    def test_malformed_post_data(self, client):
        """Test handling of malformed POST data."""
        # Test with empty form data
        response = client.post('/add', data={})
        assert response.status_code == 200
        
        # Test with None values (if possible)
        response = client.post('/add', data={
            'title': None,
            'description': None,
            'image_file_name': None
        })
        assert response.status_code == 200


class TestPerformance:
    """Test basic performance characteristics."""
    
    def test_multiple_rapid_requests(self, client):
        """Test handling of multiple rapid requests."""
        # Make multiple rapid requests to different pages
        for _ in range(10):
            response = client.get('/')
            assert response.status_code == 200
            
            response = client.get('/projects')
            assert response.status_code == 200
            
            response = client.get('/about')
            assert response.status_code == 200
    
    def test_large_project_list(self, client):
        """Test handling of large number of projects."""
        # Add multiple projects
        for i in range(20):
            project_data = {
                'title': f'Performance Test Project {i}',
                'description': f'Description for project {i}',
                'image_file_name': f'perf_{i}.jpg'
            }
            
            response = client.post('/add', data=project_data, follow_redirects=True)
            assert response.status_code == 200
        
        # View projects page
        response = client.get('/projects')
        assert response.status_code == 200
        
        # Verify all projects are displayed
        for i in range(20):
            assert f'Performance Test Project {i}'.encode() in response.data
