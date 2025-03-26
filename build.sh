#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Create static files
python -c "from flask import Flask, render_template; app = Flask(__name__); app.config['FREEZER_DESTINATION'] = 'static'; from flask_frozen import Freezer; freezer = Freezer(app); freezer.freeze()" 