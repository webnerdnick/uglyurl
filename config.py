"""
Configuration settings for UglyURL application.
"""
import os

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Uglification settings
ENCODED_URL_PARAM_NAMES = [
    'ref', 'redirect', 'target', 'url', 'destination',
    'goto', 'link', 'forward', 'next', 'return'
]

MEANINGLESS_PATHS = [
    'track', 'redirect', 'r', 'go', 'fwd', 'link', 'out',
    'click', 'visit', 'forward', 'gateway', 'portal', 'jump'
]

FAKE_UTM_SOURCES = [
    'google_ads', 'facebook_campaign', 'twitter_promo', 'linkedin_marketing',
    'email_newsletter', 'instagram_story', 'tiktok_ad', 'reddit_sponsored',
    'youtube_video', 'pinterest_pin', 'snapchat_ad', 'bing_ads'
]

FAKE_UTM_MEDIUMS = [
    'cpc', 'banner', 'email', 'social', 'affiliate', 'display',
    'video', 'native', 'retargeting', 'organic', 'referral', 'paid_search'
]

FAKE_UTM_CAMPAIGNS = [
    'spring_sale', 'summer_promo', 'fall_campaign', 'winter_special',
    'holiday_deals', 'flash_sale', 'clearance_event', 'new_launch',
    'retargeting_v2', 'awareness_campaign', 'conversion_push', 'brand_lift'
]

FAKE_UTM_CONTENTS = [
    'ad_variant_a', 'ad_variant_b', 'hero_banner', 'sidebar_ad',
    'footer_link', 'popup_modal', 'inline_text', 'image_ad',
    'video_pre_roll', 'carousel_item', 'story_swipe', 'feed_post'
]

FAKE_UTM_TERMS = [
    'buy_now', 'shop_today', 'limited_offer', 'exclusive_deal',
    'free_shipping', 'discount_code', 'save_money', 'best_price',
    'last_chance', 'trending_now', 'popular_item', 'top_seller'
]

# Security settings
ALLOWED_SCHEMES = ['http', 'https']
MAX_URL_LENGTH = 8192
BLOCKED_PATTERNS = ['javascript:', 'data:', 'file:', 'vbscript:', 'about:', 'blob:']

# Rate limiting (not implemented yet, but placeholder for future)
RATE_LIMIT_ENABLED = False
RATE_LIMIT_PER_MINUTE = 60
