"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
import sys
from flask import Flask
from service import config
from service.common import log_handlers
from flask_talisman import Talisman
from flask_cors import CORS

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


# Create Flask application
app = Flask(__name__)
app.config.from_object(config)
talisman = Talisman(app)
CORS(app)

# Import the routes After the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import, wrong-import-order
from service import routes, models  # noqa: F401 E402

# pylint: disable=wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    models.init_db(app)  # make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

app.logger.info("Service initialized!")
