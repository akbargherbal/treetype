# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the homepage!"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return f'User: {username}'

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, request

app = Flask(__name__)

@app.route('/submit_data', methods=['POST'])
def submit_data():
    if request.method == 'POST':
        return "Data received via POST!"
    return "Please use POST method."

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/items')
def get_items():
    items = [{"id": 1, "name": "Item A"}, {"id": 2, "name": "Item B"}]
    return jsonify(items)

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, request

app = Flask(__name__)

@app.route('/search')
def search_items():
    query = request.args.get('q', 'No query provided')
    return f'Searching for: {query}'

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, request

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return f'Username: {username}, Password: {password}'
    return '''<form method="post"><input type="text" name="username"><input type="password" name="password"><input type="submit"></form>'''

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/add_item', methods=['POST'])
def add_item():
    if request.is_json:
        data = request.json
        item_name = data.get('name')
        return jsonify({"message": f"Item '{item_name}' added successfully!"}), 201
    return jsonify({"error": "Request must be JSON"}), 400

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, render_template

app = Flask(__name__)

# For this snippet to run, create a 'templates' folder
# and a file 'user_profile.html' inside it, e.g.:
# <h1>Welcome, {{ username }}!</h1>

@app.route('/profile/<username>')
def user_profile(username):
    return render_template('user_profile.html', username=username)

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route('/old-dashboard')
def old_dashboard():
    return redirect(url_for('new_dashboard'))

@app.route('/new-dashboard')
def new_dashboard():
    return "Welcome to the new dashboard!"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return "Login page from Auth Blueprint"

@auth_bp.route('/register')
def register():
    return "Register page from Auth Blueprint"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, Blueprint

# Define a simple blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
    return "Login page from Auth Blueprint"

app = Flask(__name__)
app.register_blueprint(auth_bp)

@app.route('/')
def index():
    return "Main application index. Try /auth/login"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, request

app = Flask(__name__)

@app.before_request
def log_request_info():
    print(f"Request received: {request.method} {request.url}")

@app.route('/')
def home():
    return "Check your console for request info!"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.route('/')
def home():
    return "Response headers modified!"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(error):
    # For API requests, return JSON
    if request.path.startswith('/api/'):
        return jsonify({"error": "Not Found", "message": str(error)}), 404
    # For web requests, render a template (requires templates/404.html)
    return "<h1>Page Not Found</h1><p>The requested URL was not found.</p>", 404

@app.route('/')
def home():
    return "Go to a non-existent URL to see the 404 handler."

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'a_very_secret_key_for_session'

@app.route('/login/<username>')
def login(username):
    session['username'] = username
    return f"Logged in as {username}. Go to /profile to see session data."

@app.route('/profile')
def profile():
    if 'username' in session:
        return f"Welcome, {session['username']}!"
    return redirect(url_for('login', username='guest'))

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, flash, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'another_secret_key_for_flash'

# For this snippet to run, create a 'templates' folder
# and a file 'base.html' inside it, e.g.:
# {% with messages = get_flashed_messages() %}{% if messages %}<ul class=flashes>{% for message in messages %}<li>{{ message }}</li>{% endfor %}</ul>{% endif %}{% endwith %}<h1>Flash Example</h1><a href="/add-message">Add Message</a>

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/add-message')
def add_message():
    flash('This is a test message!')
    flash('Another message here.')
    return redirect(url_for('index'))

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev_key',
        DATABASE='path/to/database.db',
    )

    @app.route('/')
    def hello():
        return "Hello from the factory app!"

    return app

# To run this app:
# from your_module import create_app
# app = create_app()
# app.run()

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask

class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///prod.db'
    SECRET_KEY = 'production_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = 'sqlite:///dev.db'

app = Flask(__name__)
app.config.from_object(DevelopmentConfig) # Load configuration from an object

@app.route('/config')
def show_config():
    return f"Debug mode: {app.config['DEBUG']}, DB URI: {app.config['DATABASE_URI']}"

# PATTERN: Flask Patterns (C-Level → B-Level)

from flask import Flask, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = 'custom_decorator_secret'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected_route():
    return f"Welcome, user {session['user_id']}! This is a protected area."

@app.route('/login_page')
def login_page():
    session['user_id'] = 123 # Simulate login
    return "You are now logged in. Try /protected."