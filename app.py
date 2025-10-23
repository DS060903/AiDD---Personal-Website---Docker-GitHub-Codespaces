# IMPORTANT: Professor requires deletion of .venv folder before submission
# Please delete the .venv folder and include requirements.txt file

from flask import Flask, render_template, request, redirect, url_for
from DAL import init_db, get_all_projects, insert_project


app = Flask(__name__)

# Initialize database on startup
init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/projects")
def projects():
    projects = get_all_projects()
    return render_template("projects.html", projects=projects)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/thankyou")
def thankyou():
    # The contact form uses GET. You can access query params via request.args if needed.
    return render_template("thankyou.html")


@app.route("/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        image_file_name = request.form.get("image_file_name")
        
        if title and description and image_file_name:
            insert_project(title, description, image_file_name)
            return redirect(url_for("projects"))
    
    return render_template("add.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

