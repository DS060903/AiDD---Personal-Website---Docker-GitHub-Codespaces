import sqlite3
import os


def init_db(db_path="projects.db"):
    """
    Initialize the database and create the projects table if it doesn't exist.
    
    Args:
        db_path (str): Path to the SQLite database file
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    
    cursor = conn.cursor()
    
    # Create projects table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT NOT NULL,
            ImageFileName TEXT NOT NULL,
            CreatedAt TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def get_all_projects(db_path="projects.db"):
    """
    Retrieve all projects from the database ordered by CreatedAt DESC.
    
    Args:
        db_path (str): Path to the SQLite database file
        
    Returns:
        list: List of project rows as dict-like objects
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY CreatedAt DESC')
    
    projects = cursor.fetchall()
    conn.close()
    Projects = []
    for project in projects:
        Projects.append({
            'id': project['id'],
            'title': project['Title'],
            'description': project['Description'],
            'ImageFileName': project['ImageFileName'],
            'created_at': project['CreatedAt']
        })
    return Projects


def insert_project(title, description, image_file_name, db_path="projects.db"):
    """
    Insert a new project into the database.
    
    Args:
        title (str): Project title
        description (str): Project description
        image_file_name (str): Name of the image file
        db_path (str): Path to the SQLite database file
        
    Returns:
        int: ID of the inserted project
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
    
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO projects (Title, Description, ImageFileName)
        VALUES (?, ?, ?)
    ''', (title, description, image_file_name))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return project_id
