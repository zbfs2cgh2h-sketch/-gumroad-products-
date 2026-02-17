"""
Tests for config loader
Built by Jackson Studio
"""

import pytest
from cli.config import load_config, save_config
import tempfile
import os


def test_default_config():
    """Test default config loads"""
    config = load_config(config_file="/nonexistent/path.yaml")
    
    assert "api" in config
    assert config["api"]["endpoint"] == "https://api.example.com"


def test_yaml_config_override():
    """Test YAML config overrides defaults"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write("api:\n  endpoint: https://custom.api.com\n")
        f.flush()
        
        config = load_config(config_file=f.name)
        assert config["api"]["endpoint"] == "https://custom.api.com"
        
        os.unlink(f.name)


def test_env_override():
    """Test ENV vars override config file"""
    os.environ["API_ENDPOINT"] = "https://env.api.com"
    
    config = load_config(config_file="/nonexistent/path.yaml")
    assert config["api"]["endpoint"] == "https://env.api.com"
    
    del os.environ["API_ENDPOINT"]
