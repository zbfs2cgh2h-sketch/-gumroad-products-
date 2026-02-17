"""
Config loader with YAML/TOML/ENV support
Built by Jackson Studio
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG = {
    "api": {
        "endpoint": "https://api.example.com",
        "timeout": 30,
        "retry": 3,
    },
    "logging": {
        "level": "INFO",
        "file": "logs/app.log",
    },
    "features": {
        "auto_update": True,
    },
}


def load_config(config_file: str = None, env: str = "development") -> Dict[str, Any]:
    """
    Load config with priority: CLI args → ENV vars → config file → defaults
    
    Args:
        config_file: Path to YAML config file (default: config.yaml)
        env: Environment name (development, production, etc.)
    
    Returns:
        Merged config dict
    """
    
    config = DEFAULT_CONFIG.copy()
    
    # Load from file
    if config_file is None:
        config_file = "config.yaml"
    
    config_path = Path(config_file)
    if config_path.exists():
        with open(config_path) as f:
            file_config = yaml.safe_load(f) or {}
            
            # Support multi-environment configs
            if env in file_config:
                config.update(file_config[env])
            else:
                config.update(file_config)
    
    # Override with ENV vars (e.g., API_ENDPOINT → config["api"]["endpoint"])
    for key, value in os.environ.items():
        if key.startswith("API_"):
            config["api"][key[4:].lower()] = value
        elif key.startswith("LOG_"):
            config["logging"][key[4:].lower()] = value
    
    return config


def save_config(config: Dict[str, Any], config_file: str = "config.yaml"):
    """Save config to YAML file"""
    
    config_path = Path(config_file)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
