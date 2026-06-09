import json
import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"


def load_config():
    """Load configuration from config.json"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """Save configuration to config.json"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def get_front_prompt():
    """Get front prompt from config"""
    config = load_config()
    return config.get("FRONT_PROMPT", "Extract all text from the front side of the ID card.")

def get_back_prompt():
    """Get back prompt from config"""
    config = load_config()
    return config.get("BACK_PROMPT", "Extract all text from the back side of the ID card.")

def get_api_endpoint():
    """Get API endpoint from config"""
    config = load_config()
    return config.get("API_ENDPOINT")


def get_timeout():
    """Get timeout from config"""
    config = load_config()
    return config.get("TIMEOUT", 30)


def update_api_endpoint(endpoint):
    """Update API endpoint in config"""
    config = load_config()
    config["API_ENDPOINT"] = endpoint
    save_config(config)


def update_timeout(timeout):
    """Update timeout in config"""
    config = load_config()
    config["TIMEOUT"] = timeout
    save_config(config)
