from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
import os

app = Flask(__name__,
            template_folder="templates")

# Install Flask Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Install CSRF Protection
app.secret_key = str(os.environ['WTF_CSRF_SECRET_KEY'])
csrf = CSRFProtect(app)

import culturemesh.views

# Register Blueprints

from culturemesh.blueprints.posts.controllers import posts

app.register_blueprint(posts, url_prefix='/post')
