"""
URL Decoding and Validation Module
Extracts the original URL from ugly URLs and validates for security.
"""
import base64
from urllib.parse import urlparse, parse_qs
import config


def extract_encoded_url(query_params: dict) -> str:
    """
    Extract the encoded URL from query parameters.

    Args:
        query_params: Dictionary of query parameters (can be from parse_qs or request.args)

    Returns:
        The encoded URL string

    Raises:
        ValueError: If no encoded URL parameter is found
    """
    for param_name in config.ENCODED_URL_PARAM_NAMES:
        if param_name in query_params:
            # Handle both dict from parse_qs (returns lists) and request.args (can be single value)
            value = query_params[param_name]
            if isinstance(value, list):
                return value[0]
            return value

    raise ValueError("No encoded URL found in parameters")


def decode_original_url(encoded: str) -> str:
    """
    Decode base64url encoded URL.

    Args:
        encoded: The base64url encoded string

    Returns:
        The decoded original URL

    Raises:
        ValueError: If decoding fails
    """
    # Add padding if needed (we stripped it during encoding)
    padding = 4 - (len(encoded) % 4)
    if padding != 4:
        encoded += '=' * padding

    try:
        decoded_bytes = base64.urlsafe_b64decode(encoded)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decode URL: {e}")


def validate_url(url: str) -> bool:
    """
    Validate URL for security and proper format.

    Args:
        url: The URL to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        parsed = urlparse(url)

        # Must have a scheme
        if not parsed.scheme:
            return False

        # Only allow http and https
        if parsed.scheme not in config.ALLOWED_SCHEMES:
            return False

        # Must have a network location (domain)
        if not parsed.netloc:
            return False

        # Check for dangerous patterns
        url_lower = url.lower()
        for pattern in config.BLOCKED_PATTERNS:
            if pattern in url_lower:
                return False

        # Check length
        if len(url) > config.MAX_URL_LENGTH:
            return False

        return True
    except Exception:
        return False


def sanitize_url(url: str) -> str:
    """
    Sanitize URL by ensuring it has a proper scheme.

    Args:
        url: The URL to sanitize

    Returns:
        Sanitized URL with proper scheme
    """
    if not url.startswith(('http://', 'https://')):
        # Default to https if no scheme provided
        return 'https://' + url
    return url


def decode_ugly_url(request_args: dict) -> str:
    """
    Main decoding function. Extracts and validates the original URL from an ugly URL.

    Args:
        request_args: Query parameters from Flask request (request.args.to_dict() or similar)

    Returns:
        The original, validated URL

    Raises:
        ValueError: If URL cannot be decoded or is invalid
    """
    # Extract the encoded URL parameter
    encoded_url = extract_encoded_url(request_args)

    # Decode it
    original_url = decode_original_url(encoded_url)

    # Validate it for security
    if not validate_url(original_url):
        raise ValueError("Invalid or potentially dangerous URL")

    return original_url
