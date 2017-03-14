from flask import render_template

from app import app
from apps.utils import include


# HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# HTTP error handling
@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'), 500


# Declare imports url modules
include("apps.main.urls")
