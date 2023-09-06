"""
Flask CLI Command Extensions
"""
from service import app
from service.models import db

# Import necessary modules and define models (if any)
from flask import Flask
from service.models import Account
from service.routes import app  # Import app from your routes file

# Define Shell Context Processor and Other Setup Code
def make_shell_context():
    return {"app": app, "db": db, "Account": Account}

# Create the Flask Application Instance
app = Flask(__name__)

# Set up configuration, database connections, etc.
app.config.from_pyfile("config.py")
db.init_app(app)

# Define your routes, views, and other Flask-related code here
# ...

if __name__ == "__main__":
    app.run()

######################################################################
# Command to force tables to be rebuilt
# Usage:
#   flask db-create
######################################################################
@app.cli.command("db-create")
def db_create():
    """
    Recreates a local database. You probably should not use this on
    production. ;-)
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
