# UglyURL

The opposite of a URL shortener. Makes your URLs longer, uglier, and more confusing.

## What is UglyURL?

UglyURL is a Flask web application that transforms clean, short URLs into long, ugly ones filled with fake tracking parameters and meaningless path segments. It's the perfect tool for when you want your URLs to look like they've been through a dozen marketing campaigns.

## Features

- **Stateless Architecture**: No database required. Everything is encoded in the URL itself.
- **Configurable Ugliness**: Choose from ugliness levels 1-10 to control how ugly your URLs get.
- **Fake Tracking Parameters**: Automatically adds utm_*, fbclid, gclid, and other realistic tracking parameters.
- **Secure**: Validates URLs and only allows http/https schemes to prevent security issues.
- **Privacy-Friendly**: Your URLs are never stored. Everything is encoded and decoded on the fly.
- **Modern Web Interface**: Clean, responsive design with copy-to-clipboard functionality.

## How It Works

1. **Encode**: Your original URL is encoded using base64url (URL-safe base64)
2. **Uglify**: The encoded URL is hidden among dozens of fake tracking parameters
3. **Redirect**: When someone visits the ugly URL, they're automatically redirected to your original URL

### Example

**Before:**
```
https://example.com
```

**After (Ugliness Level 5):**
```
http://localhost:5000/track/redirect/fwd/?utm_source=google_ads&utm_medium=cpc_banner&utm_campaign=spring_sale_abc123&utm_content=ad_variant_b&utm_term=buy_now&fbclid=IwAR2XxJ8kQpLmNoPqRs&gclid=Cj0KCQiA1K6BhDx&_ga=GA1.2.123456789.987654321&_gid=GA1.2.987654321.123456789&sessionid=a1b2c3d4e5f6g7h8&ref=aHR0cHM6Ly9leGFtcGxlLmNvbQ
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd uglyurl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Web Interface

1. Enter a URL in the input field
2. Adjust the ugliness level slider (1-10)
3. Click "Uglify URL"
4. Copy your ugly URL and share it!

### API Usage (Optional)

The application is designed primarily for web interface use, but the core functions can be imported and used programmatically:

```python
from uglifier import uglify_url
from decoder import decode_ugly_url

# Uglify a URL
ugly = uglify_url('https://example.com', ugliness_level=5, base_url='http://localhost:5000')
print(ugly)

# Decode an ugly URL (from query parameters)
params = {'ref': 'aHR0cHM6Ly9leGFtcGxlLmNvbQ'}
original = decode_ugly_url(params)
print(original)
```

## Project Structure

```
uglyurl/
├── app.py              # Main Flask application
├── uglifier.py         # URL uglification logic
├── decoder.py          # URL decoding and validation
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── index.html     # Main page
│   ├── result.html    # Results page
│   └── error.html     # Error page
└── static/            # Static assets
    ├── css/
    │   └── style.css  # Stylesheet
    └── js/
        └── script.js  # JavaScript
```

## Configuration

Edit [config.py](config.py) to customize:

- **ENCODED_URL_PARAM_NAMES**: Parameter names used to store the encoded URL
- **MEANINGLESS_PATHS**: Path segments to use in ugly URLs
- **FAKE_UTM_SOURCES/MEDIUMS/etc**: Pools of fake tracking parameter values
- **ALLOWED_SCHEMES**: Whitelisted URL schemes (default: http, https)
- **MAX_URL_LENGTH**: Maximum allowed URL length
- **BLOCKED_PATTERNS**: Dangerous URL patterns to reject

## Security

UglyURL includes several security features:

- **Scheme Validation**: Only http:// and https:// URLs are allowed
- **Pattern Blocking**: Blocks dangerous schemes (javascript:, data:, file:, etc.)
- **Input Validation**: Validates URL format and length
- **XSS Prevention**: Uses Flask's auto-escaping in templates
- **No Storage**: URLs are never stored, reducing privacy concerns

## Deployment

For production deployment, use a WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Consider using:
- A reverse proxy (nginx or Apache)
- HTTPS with SSL certificates (Let's Encrypt)
- Rate limiting to prevent abuse

## Ugliness Levels Explained

- **Level 1-2**: Basic UTM parameters (source, medium, campaign)
- **Level 3-4**: Adds Facebook and Google click IDs
- **Level 5-6**: Includes analytics IDs and session tracking
- **Level 7-8**: More tracking tokens and URL encoding chaos
- **Level 9-10**: Maximum chaos with HubSpot, Mailchimp, and other fake IDs

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## License

MIT License - feel free to use this project however you like.

## Disclaimer

This tool is for entertainment and educational purposes. The fake tracking parameters are obviously fake and should not be used to impersonate real tracking systems. Use responsibly.

## Author

Created with Flask and a sense of humor about modern web tracking.
