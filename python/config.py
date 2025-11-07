"""
Configuration file for GEO Principles application
"""

import os
from typing import Dict, Any


class Config:
    """Base configuration"""

    # Flask settings
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # API settings
    API_VERSION = '1.0.0'
    API_TITLE = 'GEO Principles API'

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

    # Analysis settings
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 1024 * 1024))  # 1MB default
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')

    # Scoring thresholds
    SCORING = {
        'semantic_structure': {
            'max_score': 25,
            'weights': {
                'headings': 10,
                'paragraphs': 10,
                'lists': 5
            }
        },
        'citations': {
            'max_score': 25,
            'weights': {
                'urls': 10,
                'citation_markers': 10,
                'dates': 5
            }
        },
        'readability': {
            'max_score': 25,
            'weights': {
                'sentence_length': 10,
                'questions': 5,
                'active_voice': 10
            },
            'target_sentence_length': 20
        },
        'keywords': {
            'max_score': 25,
            'weights': {
                'content_length': 10,
                'keyword_diversity': 10,
                'statistics': 5
            },
            'min_word_count': 300
        }
    }

    # Citation validation settings
    CITATION_VALIDATION = {
        'authoritative_domains': [
            '.edu', '.gov', '.org',
            'nature.com', 'science.org', 'ieee.org',
            'arxiv.org', 'scholar.google'
        ],
        'max_citation_age_years': 10,
        'recent_threshold_years': 5
    }

    # NLP settings
    NLP = {
        'min_keyword_length': 4,
        'top_keywords_count': 10,
        'stop_words_enabled': True,
        'enable_entity_extraction': True,
        'enable_sentiment_analysis': False  # Set to True if using advanced NLP
    }

    # Rate limiting (if implemented)
    RATE_LIMIT = {
        'enabled': False,
        'requests_per_minute': 60
    }

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @staticmethod
    def get_all() -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            key: value
            for key, value in Config.__dict__.items()
            if not key.startswith('_') and not callable(value)
        }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # In production, always set SECRET_KEY via environment variable
    SECRET_KEY = os.getenv('SECRET_KEY')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(config_name: str = None) -> Config:
    """
    Get configuration object

    Args:
        config_name: Configuration name (development, testing, production)

    Returns:
        Configuration object
    """
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    return config.get(config_name, config['default'])
