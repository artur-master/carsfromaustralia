import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class DevelopmentConfig(object):
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))
    if 'MONGO_HOST' not in os.environ:
        dotenv_path = os.path.join(BASE_DIR, '.env.development')
        load_dotenv(dotenv_path)

    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY')
    JSONIFY_PRETTYPRINT_REGULAR = True
    DEBUG = True

    """MongoDB configuration"""
    MONGODB_HOST = os.getenv('MONGODB_HOST')

    """JWT configuration"""
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7
    JWT_HEADER_TYPE = 'Bearer'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    PROPAGATE_EXCEPTIONS = True


class ProductionConfig(object):
    DEBUG = False
