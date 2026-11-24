"""
Unit tests for central platform configuration.
"""
from app.config import Settings

def test_settings_defaults():
    settings = Settings()
    assert settings.PROJECT_NAME == "ALLINA IT Operations Platform"
    assert settings.VERSION == "0.1.0"
    assert "http://localhost:5173" in settings.cors_origins
    assert "http://localhost:3000" in settings.cors_origins

def test_cors_origins_parsing():
    settings = Settings(ALLOWED_ORIGINS="http://example.com, https://test.allina.ai")
    origins = settings.cors_origins
    assert len(origins) == 2
    assert "http://example.com" in origins
    assert "https://test.allina.ai" in origins
