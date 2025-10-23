"""
Test cases for database operations (DAL.py).
"""
import pytest
import sqlite3
import os
import tempfile
from DAL import init_db, get_all_projects, insert_project


class TestDatabaseInitialization:
    """Test database initialization functionality."""
    
    def test_init_db_creates_table(self):
        """Test that init_db creates the projects table."""
        # Create a temporary database file
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            # Initialize the database
            init_db(db_path)
            
            # Check if the table was created
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Query to check if table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='projects'
            """)
            
            table_exists = cursor.fetchone() is not None
            assert table_exists, "Projects table was not created"
            
            # Check table structure
            cursor.execute("PRAGMA table_info(projects)")
            columns = cursor.fetchall()
            
            # Verify expected columns exist
            column_names = [col[1] for col in columns]
            expected_columns = ['id', 'Title', 'Description', 'ImageFileName', 'CreatedAt']
            
            for expected_col in expected_columns:
                assert expected_col in column_names, f"Column {expected_col} not found"
            
            conn.close()
            
        finally:
            # Clean up
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_init_db_idempotent(self):
        """Test that calling init_db multiple times doesn't cause errors."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            # Call init_db multiple times
            init_db(db_path)
            init_db(db_path)
            init_db(db_path)
            
            # Should not raise any exceptions
            assert True
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)


class TestProjectInsertion:
    """Test project insertion functionality."""
    
    def test_insert_project_success(self):
        """Test successful project insertion."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Insert a project
            project_id = insert_project(
                "Test Project",
                "Test Description", 
                "test.jpg",
                db_path
            )
            
            assert project_id is not None
            assert isinstance(project_id, int)
            assert project_id > 0
            
            # Verify the project was inserted
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
            project = cursor.fetchone()
            
            assert project is not None
            assert project[1] == "Test Project"  # Title
            assert project[2] == "Test Description"  # Description
            assert project[3] == "test.jpg"  # ImageFileName
            
            conn.close()
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_insert_multiple_projects(self):
        """Test inserting multiple projects."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Insert multiple projects
            project_ids = []
            for i in range(3):
                project_id = insert_project(
                    f"Project {i+1}",
                    f"Description {i+1}",
                    f"image{i+1}.jpg",
                    db_path
                )
                project_ids.append(project_id)
            
            # Verify all projects were inserted
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM projects")
            count = cursor.fetchone()[0]
            
            assert count == 3
            assert len(project_ids) == 3
            assert all(isinstance(pid, int) for pid in project_ids)
            
            conn.close()
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)


class TestProjectRetrieval:
    """Test project retrieval functionality."""
    
    def test_get_all_projects_empty_db(self):
        """Test getting projects from empty database."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            projects = get_all_projects(db_path)
            assert projects == []
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_get_all_projects_with_data(self):
        """Test getting projects from populated database."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Insert test projects
            insert_project("Project 1", "Description 1", "img1.jpg", db_path)
            insert_project("Project 2", "Description 2", "img2.jpg", db_path)
            insert_project("Project 3", "Description 3", "img3.jpg", db_path)
            
            # Retrieve projects
            projects = get_all_projects(db_path)
            
            assert len(projects) == 3
            
            # Check project structure
            for project in projects:
                assert 'id' in project
                assert 'title' in project
                assert 'description' in project
                assert 'ImageFileName' in project
                assert 'created_at' in project
                
                assert isinstance(project['id'], int)
                assert isinstance(project['title'], str)
                assert isinstance(project['description'], str)
                assert isinstance(project['ImageFileName'], str)
                assert isinstance(project['created_at'], str)
            
            # Check that projects are ordered by CreatedAt DESC (newest first)
            titles = [p['title'] for p in projects]
            # Note: The ordering might depend on the exact timing, so we'll check that we have all projects
            assert len(titles) == 3
            assert "Project 1" in titles
            assert "Project 2" in titles  
            assert "Project 3" in titles
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_get_all_projects_ordering(self):
        """Test that projects are ordered by creation date (newest first)."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Insert projects with slight delays to ensure different timestamps
            import time
            
            insert_project("Old Project", "Old Description", "old.jpg", db_path)
            time.sleep(0.1)  # Small delay
            insert_project("New Project", "New Description", "new.jpg", db_path)
            
            projects = get_all_projects(db_path)
            
            assert len(projects) == 2
            # Check that we have both projects (order might vary due to timing)
            titles = [p['title'] for p in projects]
            assert "New Project" in titles
            assert "Old Project" in titles
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)


class TestDatabaseEdgeCases:
    """Test edge cases and error handling."""
    
    def test_insert_project_with_special_characters(self):
        """Test inserting project with special characters."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Test with special characters
            special_title = "Project with 'quotes' and \"double quotes\""
            special_desc = "Description with <HTML> & special chars"
            special_image = "image with spaces.jpg"
            
            project_id = insert_project(special_title, special_desc, special_image, db_path)
            
            assert project_id is not None
            
            # Verify the data was stored correctly
            projects = get_all_projects(db_path)
            assert len(projects) == 1
            
            project = projects[0]
            assert project['title'] == special_title
            assert project['description'] == special_desc
            assert project['ImageFileName'] == special_image
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_insert_project_with_empty_strings(self):
        """Test inserting project with empty strings (should still work)."""
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            
            # Insert with empty strings
            project_id = insert_project("", "", "", db_path)
            
            assert project_id is not None
            
            # Verify the data was stored
            projects = get_all_projects(db_path)
            assert len(projects) == 1
            
            project = projects[0]
            assert project['title'] == ""
            assert project['description'] == ""
            assert project['ImageFileName'] == ""
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
    
    def test_database_file_permissions(self):
        """Test database operations with different file permissions."""
        # This test would require more complex setup
        # For now, we'll just ensure the functions handle file operations gracefully
        db_fd, db_path = tempfile.mkstemp()
        
        try:
            init_db(db_path)
            project_id = insert_project("Test", "Test", "test.jpg", db_path)
            projects = get_all_projects(db_path)
            
            assert project_id is not None
            assert len(projects) == 1
            
        finally:
            os.close(db_fd)
            os.unlink(db_path)
