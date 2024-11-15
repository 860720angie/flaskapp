from flask import Flask

app = Flask(__name__)

# Import routes at the end to avoid circular imports
from app import routes

