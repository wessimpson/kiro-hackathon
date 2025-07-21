"""
Test configuration and settings
"""
import pytest
from src.config.settings import Settings


def test_settings_creation():
    """Test that settings can be created with default values"""
    settings = Settings()
    assert settings.app_name == "AI Job Application Assistant"
    assert settings.debug is False
    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.openai_model == "gpt-4"


def test_settings_with_env_override():
    """Test that environment variables override defaults"""
    import os
    os.environ["APP_NAME"] = "Test App"
    os.environ["DEBUG"] = "true"
    
    settings = Settings()
    assert settings.app_name == "Test App"
    assert settings.debug is True
    
    # Clean up
    del os.environ["APP_NAME"]
    del os.environ["DEBUG"]


if __name__ == "__main__":
    pytest.main([__file__])