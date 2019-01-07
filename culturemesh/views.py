"""
Contains the views and templates for the top-level site. This includes:
  - The home page
  - The about page
  - The registration page
  - The login page
"""
import config
from flask import render_template, session
from culturemesh import app


@app.route("/")
@app.route("/index/")
def home():
    return render_template('index.html')


@app.after_request
def add_custom_http_response_headers(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=86400; includeSubDomains"
    response.headers["Expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' https://www.culturemesh.com;"
    response.headers["X-CultureMesh"] = "lite"
    return response


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = config.PERMANENT_SESSION_LIFETIME
