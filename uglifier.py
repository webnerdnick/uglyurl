"""
URL Uglification Engine
Transforms clean URLs into long, ugly ones with fake tracking parameters.
"""
import base64
import secrets
import random
from urllib.parse import urlencode, quote
import config


def encode_original_url(url: str) -> str:
    """
    Encode original URL using base64url encoding.

    Args:
        url: The original URL to encode

    Returns:
        URL-safe base64 encoded string without padding
    """
    url_bytes = url.encode('utf-8')
    encoded = base64.urlsafe_b64encode(url_bytes)
    # Remove padding for extra ugliness
    return encoded.decode('utf-8').rstrip('=')


def generate_fake_tracking_params(ugliness_level: int) -> dict:
    """
    Generate fake tracking parameters based on ugliness level.

    Args:
        ugliness_level: How ugly to make it (1-10)

    Returns:
        Dictionary of parameter name -> value
    """
    params = {}

    # Level 1+: Basic UTM parameters
    if ugliness_level >= 1:
        params['utm_source'] = random.choice(config.FAKE_UTM_SOURCES)
        params['utm_medium'] = random.choice(config.FAKE_UTM_MEDIUMS)

    # Level 2+: Campaign and content
    if ugliness_level >= 2:
        campaign = random.choice(config.FAKE_UTM_CAMPAIGNS)
        params['utm_campaign'] = f'{campaign}_{secrets.token_hex(2)}'
        params['utm_content'] = random.choice(config.FAKE_UTM_CONTENTS)

    # Level 3+: Facebook click ID
    if ugliness_level >= 3:
        params['utm_term'] = random.choice(config.FAKE_UTM_TERMS)
        params['fbclid'] = f'IwAR{secrets.token_urlsafe(16)}'

    # Level 4+: Google click ID and session
    if ugliness_level >= 4:
        params['gclid'] = f'Cj0KCQ{secrets.token_urlsafe(12)}'
        params['_ga'] = f'GA1.2.{random.randint(100000000, 999999999)}.{random.randint(100000000, 999999999)}'

    # Level 5+: More analytics IDs
    if ugliness_level >= 5:
        params['_gid'] = f'GA1.2.{random.randint(100000000, 999999999)}.{random.randint(100000000, 999999999)}'
        params['sessionid'] = secrets.token_hex(16)

    # Level 6+: Microsoft click ID
    if ugliness_level >= 6:
        params['msclkid'] = secrets.token_urlsafe(16)
        params['tracking_token'] = f'TRK_{secrets.token_urlsafe(12)}'

    # Level 7+: More tracking nonsense
    if ugliness_level >= 7:
        params['impression_id'] = secrets.token_hex(8)
        params['click_id'] = f'CLK_{secrets.token_hex(8)}'
        params['visitor_id'] = secrets.token_hex(12)

    # Level 8+: Even more parameters
    if ugliness_level >= 8:
        params['referrer_id'] = f'REF_{secrets.token_hex(8)}'
        params['affiliate_code'] = secrets.token_urlsafe(10)
        params['partner_id'] = f'P{random.randint(1000, 9999)}'

    # Level 9+: Timestamp and version info
    if ugliness_level >= 9:
        params['timestamp'] = str(random.randint(1700000000, 1800000000))
        params['version'] = f'v{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 99)}'
        params['build'] = str(random.randint(1000, 9999))

    # Level 10: Maximum chaos - add random nonsense
    if ugliness_level >= 10:
        params['_hsenc'] = secrets.token_urlsafe(20)  # HubSpot
        params['_hsmi'] = str(random.randint(100000, 999999))
        params['mc_cid'] = secrets.token_hex(16)  # Mailchimp
        params['mc_eid'] = secrets.token_hex(16)
        params['rb_clickid'] = secrets.token_urlsafe(12)  # Random "click ID"
        params['wickedid'] = secrets.token_hex(10)  # Wicked Reports

    return params


def generate_meaningless_path(ugliness_level: int) -> str:
    """
    Generate random meaningless path segments.

    Args:
        ugliness_level: How ugly to make it (1-10)

    Returns:
        Path string with random segments
    """
    if ugliness_level < 3:
        return '/r'

    # Number of path segments increases with ugliness
    num_segments = min((ugliness_level // 2) + 1, len(config.MEANINGLESS_PATHS))
    segments = random.sample(config.MEANINGLESS_PATHS, num_segments)

    # Optionally add a fake file extension
    path = '/' + '/'.join(segments)

    if ugliness_level >= 8:
        # Add fake file extension
        extensions = ['.php', '.aspx', '.jsp', '.do', '.action']
        path += random.choice(extensions)

    return path


def apply_url_encoding_chaos(query_string: str) -> str:
    """
    Apply unnecessary URL encoding to parts of the query string.

    Args:
        query_string: The query string to encode

    Returns:
        Query string with chaotic encoding
    """
    result = []
    for char in query_string:
        # Randomly encode characters that don't need encoding
        if char in 'abcdefghijklmnopqrstuvwxyz0123456789' and random.random() < 0.3:
            result.append(f'%{ord(char):02X}')
        else:
            result.append(char)
    return ''.join(result)


def generate_fragment_noise(ugliness_level: int) -> str:
    """
    Generate fake fragment identifiers.

    Args:
        ugliness_level: How ugly to make it

    Returns:
        Fragment string (with # prefix) or empty string
    """
    if ugliness_level < 6:
        return ''

    fragment_types = [
        f'track_impression_{secrets.token_hex(4)}',
        f'ref_{secrets.token_hex(6)}',
        f'anchor_{random.randint(1000, 9999)}',
        f'section_{secrets.token_urlsafe(6)}',
        f'view_{secrets.token_hex(5)}',
    ]

    return '#' + random.choice(fragment_types)


def uglify_url(original_url: str, ugliness_level: int = 5, base_url: str = 'http://localhost:5000') -> str:
    """
    Main uglification function. Transforms a clean URL into an ugly one.

    Args:
        original_url: The URL to uglify
        ugliness_level: How ugly to make it (1-10)
        base_url: The base URL of this application

    Returns:
        The uglified URL
    """
    # Clamp ugliness level
    ugliness_level = max(1, min(10, ugliness_level))

    # Encode the original URL
    encoded = encode_original_url(original_url)

    # Generate fake tracking parameters
    params = generate_fake_tracking_params(ugliness_level)

    # Add the encoded URL to parameters with a random parameter name
    encoded_param_name = random.choice(config.ENCODED_URL_PARAM_NAMES)
    params[encoded_param_name] = encoded

    # Shuffle the parameters for extra chaos
    param_items = list(params.items())
    random.shuffle(param_items)

    # Generate meaningless path
    path = generate_meaningless_path(ugliness_level)

    # Build query string
    query_string = urlencode(param_items)

    # Apply URL encoding chaos if high ugliness
    if ugliness_level >= 8:
        query_string = apply_url_encoding_chaos(query_string)

    # Add fragment if ugly enough
    fragment = generate_fragment_noise(ugliness_level)

    # Construct final ugly URL
    ugly_url = f'{base_url.rstrip("/")}{path}?{query_string}{fragment}'

    return ugly_url
