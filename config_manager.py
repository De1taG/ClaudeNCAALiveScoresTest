"""Configuration manager for NCAA Sports Tracker"""
import json
import os
from pathlib import Path


class ConfigManager:
    """Manages application configuration and persistent settings"""

    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._default_config()
        return self._default_config()

    def _default_config(self):
        """Return default configuration"""
        return {
            "last_save_directory": str(Path.home()),
            "update_interval": 60,
            "default_sport": "WBB",
            "default_division": 1,
            "default_season_year": 2025
        }

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
        self.save_config()
