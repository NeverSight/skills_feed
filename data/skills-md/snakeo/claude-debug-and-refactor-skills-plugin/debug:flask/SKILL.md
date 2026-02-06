---
name: debug:flask
description: Debug Flask applications systematically with this comprehensive troubleshooting skill. Covers routing errors (404/405), Jinja2 template issues, application context problems, SQLAlchemy session management, blueprint registration failures, and circular import resolution. Provides structured four-phase debugging methodology with Flask-specific tools including Werkzeug debugger, Flask-DebugToolbar, and Flask shell for interactive investigation.
---

# Flask Debugging Guide

A systematic approach to debugging Flask applications using established patterns and Flask-specific tooling.

## Common Error Patterns

### HTTP Status Code Errors

**404 Not Found - Routing Issues**
- Route decorator not matching requested URL
- Typos in route definitions or endpoint names
- Blueprint not registered with application
- Missing trailing slash mismatch (`strict_slashes` setting)
- URL rules registered after first request

**500 Internal Server Error**
- Unhandled exceptions in view functions
- Template rendering errors
- Database connection failures
- Malformed JSON request data (missing `Content-Type: application/json`)
- Circular imports preventing app initialization

**405 Method Not Allowed**
- HTTP method not specified in `@app.route()` methods parameter
- Form submission using wrong method (GET vs POST)

### Jinja2 Template Errors

**TemplateNotFound**
- Template not in `templates/` directory
- Custom template folder not configured
- Blueprint template folder misconfigured

**UndefinedError**
- Variable not passed to `render_template()`
- Typo in template variable name
- Accessing attribute on None object

**TemplateSyntaxError**
- Unclosed blocks (`{% if %}` without `{% endif %}`)
- Invalid filter usage
- Incorrect macro definitions

### Application Context Errors

**RuntimeError: Working outside of application context**
- Accessing `current_app` outside request/CLI context
- Database operations outside `with app.app_context():`
- Celery tasks not properly configured with app context

**RuntimeError: Working outside of request context**
- Accessing `request`, `session`, or `g` outside view function
- Background thread without request context

### SQLAlchemy Session Issues

**DetachedInstanceError**
- Accessing lazy-loaded relationship outside session
- Object expired after transaction commit
- Session closed prematurely

**InvalidRequestError: Object already attached to session**
- Adding object already in different session
- Improper session management in tests

**OperationalError: Connection pool exhausted**
- Connections not being returned to pool
- Missing `db.session.close()` or `db.session.remove()`
- Long-running transactions

### Blueprint Registration Problems

**Blueprint registration failures**
- Circular imports between blueprints
- Duplicate blueprint names
- Blueprint registered after first request
- URL prefix conflicts

### Import and Module Errors

**ImportError: cannot import name 'Flask'**
- Circular dependency in modules
- File named `flask.py` shadowing the package
- Virtual environment not activated

**ModuleNotFoundError: No module named 'flask'**
- Virtual environment not activated
- Flask not installed in current environment
- Wrong Python interpreter

## Debugging Tools

### Built-in Flask Debugger (Werkzeug)

```python
# Enable debug mode (DEVELOPMENT ONLY - NEVER IN PRODUCTION)
# Method 1: Environment variable
# export FLASK_DEBUG=1

# Method 2: In code (not recommended)
app.run(debug=True)

# Method 3: Flask CLI
# flask run --debug
```

The Werkzeug debugger provides:
- Interactive traceback with code context
- In-browser Python REPL at each stack frame
- Variable inspection at each level
- PIN-protected access (check terminal for PIN)

**Security Warning**: Never enable debug mode in production. The debugger allows arbitrary code execution from the browser.

### Python Debugger (pdb/breakpoint)

```python
# Insert breakpoint in code
def my_view():
    data = get_data()
    breakpoint()  # Python 3.7+ (or: import pdb; pdb.set_trace())
    return process(data)

# Common pdb commands:
# n (next) - Execute next line
# s (step) - Step into function
# c (continue) - Continue to next breakpoint
# p variable - Print variable value
# pp variable - Pretty print variable
# l (list) - Show current code context
# w (where) - Show stack trace
# q (quit) - Quit debugger
```

### Flask Shell

```bash
# Start interactive shell with app context
flask shell

# In shell:
>>> from app.models import User
>>> User.query.all()
>>> app.config['DEBUG']
>>> app.url_map  # View all registered routes
```

### Logging Module

```python
import logging
from flask import Flask

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Add file handler for persistent logs
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)

# Usage in views
@app.route('/api/data')
def get_data():
    app.logger.debug('Processing request for /api/data')
    try:
        result = fetch_data()
        app.logger.info(f'Successfully fetched {len(result)} records')
        return jsonify(result)
    except Exception as e:
        app.logger.error(f'Error fetching data: {e}', exc_info=True)
        raise
```

### Flask-DebugToolbar

```python
# Install: pip install flask-debugtoolbar

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
```

Provides sidebar panels for:
- Request/response headers
- Template rendering details
- SQLAlchemy queries (with query time)
- Route matching information
- Configuration values
- Logging messages

### SQLAlchemy Query Logging

```python
# Enable SQL query logging
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Or in Flask config
app.config['SQLALCHEMY_ECHO'] = True

# For query analysis with flask-debugtoolbar
app.config['DEBUG_TB_PANELS'] = [
    'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
]
```

## The Four Phases of Flask Debugging

### Phase 1: Reproduce and Isolate

**Capture the exact error state:**

```bash
# Check Flask is running with debug enabled
flask run --debug

# View registered routes
flask routes

# Check configuration
flask shell
>>> app.config
```

**Minimal reproduction:**

```python
# Create minimal test case
def test_failing_route(client):
    response = client.get('/api/broken-endpoint')
    print(f"Status: {response.status_code}")
    print(f"Data: {response.get_data(as_text=True)}")
    assert response.status_code == 200
```

**Questions to answer:**
- Does error occur on every request or intermittently?
- What is the exact HTTP status code?
- What does the traceback show?
- What was the request payload?
- What environment variables are set?

### Phase 2: Gather Information

**Collect comprehensive context:**

```python
# Add request logging middleware
@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', dict(request.headers))
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('Args: %s', dict(request.args))

@app.after_request
def log_response_info(response):
    app.logger.debug('Response Status: %s', response.status)
    return response
```

**Check configuration:**

```bash
flask shell
>>> from flask import current_app
>>> current_app.config['SQLALCHEMY_DATABASE_URI']
>>> current_app.url_map
>>> current_app.extensions
```

**Database state:**

```python
# In flask shell
>>> from app import db
>>> db.session.execute(text("SELECT 1")).fetchone()  # Test connection
>>> User.query.count()
>>> db.engine.pool.status()  # Connection pool status
```

### Phase 3: Hypothesize and Test

**Form hypotheses based on error patterns:**

| Error Pattern | Likely Cause | Test |
|---------------|--------------|------|
| 404 on valid route | Blueprint not registered | Check `app.url_map` |
| 500 with no traceback | Error before request context | Check `create_app()` |
| DetachedInstanceError | Lazy load outside session | Add `lazy='joined'` |
| Connection refused | DB not running | Test connection string |

**Test hypotheses systematically:**

```python
# Hypothesis: Route not registered
flask routes | grep expected_endpoint

# Hypothesis: Database connection issue
flask shell
>>> from app import db
>>> db.session.execute(text("SELECT 1"))

# Hypothesis: Configuration not loaded
flask shell
>>> import os
>>> os.environ.get('DATABASE_URL')
>>> app.config.get('DATABASE_URL')
```

### Phase 4: Fix and Verify

**Apply fix with minimal changes:**

```python
# Before fixing, add test to capture expected behavior
def test_user_creation(client):
    response = client.post('/api/users', json={'name': 'Test'})
    assert response.status_code == 201
    assert 'id' in response.get_json()

# After fix, verify test passes
pytest tests/test_users.py::test_user_creation -v
```

**Verify fix doesn't introduce regressions:**

```bash
# Run full test suite
pytest

# Run with coverage to ensure fix is tested
pytest --cov=app --cov-report=term-missing
```

**Document the fix:**

```python
# Add comment explaining the fix
@app.route('/api/users', methods=['POST'])
def create_user():
    # FIX: Must validate JSON before accessing request.json
    # See: https://github.com/org/repo/issues/123
    if not request.is_json:
        return jsonify(error='Content-Type must be application/json'), 400
    ...
```

## Quick Reference Commands

```bash
# View all registered routes
flask routes

# Interactive shell with app context
flask shell

# Database migration status (Flask-Migrate)
flask db status
flask db current
flask db history

# Run with debug mode
flask run --debug

# Run with specific host/port
flask run --host=0.0.0.0 --port=5000

# Show Flask configuration
flask shell -c "print(app.config)"

# Test database connection
flask shell -c "from app import db; print(db.session.execute(text('SELECT 1')).fetchone())"

# Check environment variables
flask shell -c "import os; print(os.environ.get('FLASK_ENV'))"

# List installed extensions
flask shell -c "print(list(app.extensions.keys()))"
```

## Flask-Specific Debugging Patterns

### Debug Application Factory Issues

```python
# Common issue: app not created properly
def create_app(config_name='default'):
    app = Flask(__name__)

    # Debug: Print when config loads
    print(f"Loading config: {config_name}")
    app.config.from_object(config[config_name])

    # Debug: Verify extensions initialized
    db.init_app(app)
    print(f"DB initialized: {db}")

    # Debug: Verify blueprints registered
    from app.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    print(f"Registered routes: {[r.rule for r in app.url_map.iter_rules()]}")

    return app
```

### Debug Request/Response Cycle

```python
from flask import g, request
import time

@app.before_request
def before_request():
    g.start_time = time.time()
    g.request_id = request.headers.get('X-Request-ID', 'unknown')
    app.logger.info(f"[{g.request_id}] {request.method} {request.path}")

@app.after_request
def after_request(response):
    duration = time.time() - g.start_time
    app.logger.info(
        f"[{g.request_id}] {response.status_code} ({duration:.3f}s)"
    )
    return response

@app.teardown_request
def teardown_request(exception):
    if exception:
        app.logger.error(f"[{g.request_id}] Exception: {exception}")
```

### Debug SQLAlchemy N+1 Queries

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()

# Log all queries in development
if app.debug:
    @event.listens_for(db.engine, "before_cursor_execute")
    def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        app.logger.debug(f"SQL: {statement}")
        app.logger.debug(f"Params: {parameters}")
```

### Debug Template Rendering

```python
# Add context processor to expose debug info
@app.context_processor
def debug_context():
    if app.debug:
        return {
            'debug_info': {
                'endpoint': request.endpoint,
                'view_args': request.view_args,
                'url': request.url,
            }
        }
    return {}
```

```html
<!-- In template, show debug info -->
{% if config.DEBUG %}
<pre>
Endpoint: {{ debug_info.endpoint }}
View Args: {{ debug_info.view_args }}
URL: {{ debug_info.url }}
</pre>
{% endif %}
```

### Debug Blueprint Registration

```python
def register_blueprints(app):
    """Register all blueprints with debugging."""
    from app.api import api_bp
    from app.auth import auth_bp

    blueprints = [
        (api_bp, '/api'),
        (auth_bp, '/auth'),
    ]

    for bp, prefix in blueprints:
        app.logger.debug(f"Registering blueprint: {bp.name} at {prefix}")
        try:
            app.register_blueprint(bp, url_prefix=prefix)
            app.logger.debug(f"Successfully registered {bp.name}")
        except Exception as e:
            app.logger.error(f"Failed to register {bp.name}: {e}")
            raise
```

## Error Handlers for Better Debugging

```python
from flask import jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all unhandled exceptions."""
    # Log the full exception with traceback
    app.logger.exception(f"Unhandled exception: {e}")

    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return jsonify(error=e.description), e.code

    # Return generic error in production, detailed in development
    if app.debug:
        return jsonify(
            error=str(e),
            type=type(e).__name__,
            traceback=traceback.format_exc()
        ), 500

    return jsonify(error="Internal server error"), 500

@app.errorhandler(404)
def not_found(e):
    app.logger.warning(f"404: {request.url}")
    return jsonify(error="Resource not found", path=request.path), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()  # Rollback any failed transactions
    app.logger.error(f"500 error: {e}")
    return jsonify(error="Internal server error"), 500
```

## Production Debugging with Sentry

```python
# Install: pip install sentry-sdk[flask]

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[
        FlaskIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,  # 10% of transactions for performance monitoring
    environment=os.environ.get('FLASK_ENV', 'production'),
)
```

## Environment-Specific Configuration

```python
class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-prod')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """Development configuration with debugging enabled."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration - no debug features."""
    DEBUG = False
    SQLALCHEMY_ECHO = False

    # Use proper secret key
    SECRET_KEY = os.environ['SECRET_KEY']  # Will raise if not set

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
```

## Debugging Checklist

Before escalating or spending extensive time:

- [ ] Is Flask running in debug mode? (`FLASK_DEBUG=1`)
- [ ] Are you in the correct virtual environment?
- [ ] Is the database running and accessible?
- [ ] Have you checked the full traceback in the terminal?
- [ ] Did you run `flask routes` to verify route registration?
- [ ] Is the request Content-Type correct for JSON endpoints?
- [ ] Have you checked for circular imports?
- [ ] Are all required environment variables set?
- [ ] Is the SECRET_KEY configured?
- [ ] Have you tried `flask shell` to test in isolation?
- [ ] Did you check the browser's Network tab for request details?
- [ ] Are database migrations up to date? (`flask db upgrade`)

## References

- [Flask Official Debugging Documentation](https://flask.palletsprojects.com/en/stable/debugging/)
- [Flask Error Handling Guide](https://flask.palletsprojects.com/en/stable/errorhandling/)
- [Flask Mega-Tutorial: Error Handling](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling)
- [Flask Error Handling Patterns - Better Stack](https://betterstack.com/community/guides/scaling-python/flask-error-handling/)
- [DigitalOcean: Handle Errors in Flask](https://www.digitalocean.com/community/tutorials/how-to-handle-errors-in-a-flask-application)
