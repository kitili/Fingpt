"""
Configuration Settings
=====================

Configuration management for FinGPT project.
Demonstrates: Configuration management, environment variables, settings patterns
"""

import os
from typing import Optional
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class DatabaseConfig:
    """Database configuration"""
    url: str = os.getenv("DATABASE_URL", "sqlite:///fingpt.db")
    echo: bool = os.getenv("DATABASE_ECHO", "False").lower() == "true"

@dataclass
class APIConfig:
    """API configuration"""
    host: str = os.getenv("API_HOST", "0.0.0.0")
    port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("API_DEBUG", "False").lower() == "true"
    cors_origins: list = os.getenv("CORS_ORIGINS", "*").split(",")

@dataclass
class MarketDataConfig:
    """Market data configuration"""
    default_period: str = os.getenv("DEFAULT_PERIOD", "1y")
    max_workers: int = int(os.getenv("MAX_WORKERS", "5"))
    cache_duration: int = int(os.getenv("CACHE_DURATION", "300"))  # 5 minutes

@dataclass
class SentimentConfig:
    """Sentiment analysis configuration"""
    model_name: str = os.getenv("SENTIMENT_MODEL", "default")
    confidence_threshold: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.5"))
    batch_size: int = int(os.getenv("BATCH_SIZE", "100"))

@dataclass
class PortfolioConfig:
    """Portfolio optimization configuration"""
    risk_free_rate: float = float(os.getenv("RISK_FREE_RATE", "0.02"))
    max_position_weight: float = float(os.getenv("MAX_POSITION_WEIGHT", "0.4"))
    min_position_weight: float = float(os.getenv("MIN_POSITION_WEIGHT", "0.0"))

@dataclass
class LoggingConfig:
    """Logging configuration"""
    level: str = os.getenv("LOG_LEVEL", "INFO")
    format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_path: Optional[str] = os.getenv("LOG_FILE")

@dataclass
class Settings:
    """Main settings class"""
    database: DatabaseConfig = DatabaseConfig()
    api: APIConfig = APIConfig()
    market_data: MarketDataConfig = MarketDataConfig()
    sentiment: SentimentConfig = SentimentConfig()
    portfolio: PortfolioConfig = PortfolioConfig()
    logging: LoggingConfig = LoggingConfig()
    
    # Application settings
    app_name: str = "FinGPT for Everyone"
    app_version: str = "1.0.0"
    app_description: str = "CS Solutions in Finance"
    
    # Feature flags
    enable_sentiment_analysis: bool = os.getenv("ENABLE_SENTIMENT", "True").lower() == "true"
    enable_portfolio_optimization: bool = os.getenv("ENABLE_PORTFOLIO", "True").lower() == "true"
    enable_backtesting: bool = os.getenv("ENABLE_BACKTESTING", "True").lower() == "true"
    enable_api: bool = os.getenv("ENABLE_API", "True").lower() == "true"

# Global settings instance
settings = Settings()

def get_settings() -> Settings:
    """Get settings instance"""
    return settings

def update_setting(section: str, key: str, value: any) -> None:
    """Update a setting value"""
    if hasattr(settings, section):
        section_obj = getattr(settings, section)
        if hasattr(section_obj, key):
            setattr(section_obj, key, value)
        else:
            raise ValueError(f"Key '{key}' not found in section '{section}'")
    else:
        raise ValueError(f"Section '{section}' not found")

def get_setting(section: str, key: str) -> any:
    """Get a setting value"""
    if hasattr(settings, section):
        section_obj = getattr(settings, section)
        if hasattr(section_obj, key):
            return getattr(section_obj, key)
        else:
            raise ValueError(f"Key '{key}' not found in section '{section}'")
    else:
        raise ValueError(f"Section '{section}' not found")

# Environment-specific configurations
def get_development_settings() -> Settings:
    """Get development-specific settings"""
    dev_settings = Settings()
    dev_settings.api.debug = True
    dev_settings.logging.level = "DEBUG"
    dev_settings.database.echo = True
    return dev_settings

def get_production_settings() -> Settings:
    """Get production-specific settings"""
    prod_settings = Settings()
    prod_settings.api.debug = False
    prod_settings.logging.level = "WARNING"
    prod_settings.database.echo = False
    return prod_settings

def get_test_settings() -> Settings:
    """Get test-specific settings"""
    test_settings = Settings()
    test_settings.database.url = "sqlite:///:memory:"
    test_settings.api.debug = True
    test_settings.logging.level = "DEBUG"
    return test_settings

# Configuration validation
def validate_settings(settings: Settings) -> bool:
    """Validate settings configuration"""
    try:
        # Validate API settings
        if settings.api.port < 1 or settings.api.port > 65535:
            raise ValueError("Invalid API port")
        
        # Validate portfolio settings
        if settings.portfolio.risk_free_rate < 0 or settings.portfolio.risk_free_rate > 1:
            raise ValueError("Invalid risk-free rate")
        
        if settings.portfolio.max_position_weight < 0 or settings.portfolio.max_position_weight > 1:
            raise ValueError("Invalid max position weight")
        
        if settings.portfolio.min_position_weight < 0 or settings.portfolio.min_position_weight > 1:
            raise ValueError("Invalid min position weight")
        
        if settings.portfolio.min_position_weight >= settings.portfolio.max_position_weight:
            raise ValueError("Min position weight must be less than max position weight")
        
        # Validate market data settings
        if settings.market_data.max_workers < 1:
            raise ValueError("Max workers must be at least 1")
        
        if settings.market_data.cache_duration < 0:
            raise ValueError("Cache duration must be non-negative")
        
        return True
        
    except Exception as e:
        print(f"Settings validation failed: {e}")
        return False

# Initialize and validate settings
if not validate_settings(settings):
    print("Warning: Settings validation failed, using default values")

# Export commonly used settings
DATABASE_URL = settings.database.url
API_HOST = settings.api.host
API_PORT = settings.api.port
DEBUG = settings.api.debug
LOG_LEVEL = settings.logging.level
