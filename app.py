"""
UglyURL - The URL Uglifier
Flask application that makes URLs longer and uglier.
"""
from flask import Flask, render_template, request, redirect, url_for
from uglifier import uglify_url
from decoder import decode_ugly_url, sanitize_url
import config

app = Flask(__name__)
app.config.from_object(config)


@app.route('/', methods=['GET'])
def index():
    """Render the main page with URL input form."""
    return render_template('index.html')


@app.route('/uglify', methods=['POST'])
def uglify():
    """
    Handle URL uglification request.
    Accepts form data with 'url' and 'ugliness' parameters.
    """
    original_url = request.form.get('url', '').strip()
    ugliness_level = request.form.get('ugliness', '5')

    # Validate input
    if not original_url:
        return render_template('error.html',
                             error='Please provide a URL',
                             back_url=url_for('index')), 400

    # Convert ugliness to int
    try:
        ugliness_level = int(ugliness_level)
    except ValueError:
        ugliness_level = 5

    # Ensure URL has proper scheme
    original_url = sanitize_url(original_url)

    try:
        # Get base URL from request (handles localhost and production)
        base_url = request.url_root.rstrip('/')

        # Generate ugly URL
        ugly_url = uglify_url(original_url, ugliness_level, base_url)

        # Calculate statistics
        original_length = len(original_url)
        ugly_length = len(ugly_url)
        increase = ugly_length - original_length
        increase_pct = (increase / original_length) * 100 if original_length > 0 else 0

        return render_template('result.html',
                             original_url=original_url,
                             ugly_url=ugly_url,
                             original_length=original_length,
                             ugly_length=ugly_length,
                             increase=increase,
                             increase_pct=increase_pct,
                             ugliness_level=ugliness_level)

    except Exception as e:
        return render_template('error.html',
                             error=f'Failed to uglify URL: {str(e)}',
                             back_url=url_for('index')), 500


@app.route('/<path:ugly_path>', methods=['GET'])
def handle_ugly_url(ugly_path):
    """
    Handle requests to ugly URLs and redirect to the original URL.
    The path itself doesn't matter - we extract the original URL from query parameters.
    """
    try:
        # Decode the ugly URL using query parameters
        original_url = decode_ugly_url(request.args.to_dict())

        # Redirect to the original URL
        return redirect(original_url, code=302)

    except ValueError as e:
        return render_template('error.html',
                             error=f'Invalid ugly URL: {str(e)}',
                             back_url=url_for('index')), 400
    except Exception as e:
        return render_template('error.html',
                             error='Failed to process ugly URL',
                             back_url=url_for('index')), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('error.html',
                         error='Page not found',
                         back_url=url_for('index')), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return render_template('error.html',
                         error='Internal server error',
                         back_url=url_for('index')), 500


if __name__ == '__main__':
    # Run the Flask development server
    # In production, use a proper WSGI server like Gunicorn
    app.run(debug=True, host='0.0.0.0', port=5000)
