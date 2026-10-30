"""
Question 6: Hierarchical Configuration Management System
Topic: JSON, CSV, Web APIs, and Databases

Key Concepts Tested:
- configparser.ConfigParser with interpolation and INI section management
- Strongly typed getters (get_int, get_bool, get_float, get_string)
- Hierarchical configuration precedence: Env Var > INI Config > Fallback
- JSON configuration export and persistence
- Validation and error handling for missing configuration keys
"""

import os
import json
import configparser
from typing import Optional, Dict, Any


class ConfigMissingError(Exception):
    """Raised when a mandatory configuration section or key is missing."""
    pass


class ConfigManager:
    """
    Configuration manager providing INI parsing, environment overrides,
    strongly typed accessors, and JSON export.
    """

    def __init__(self) -> None:
        self._config = configparser.ConfigParser(interpolation=configparser.BasicInterpolation())
        self._env_overrides: Dict[str, Dict[str, str]] = {}

    def load_ini_string(self, ini_text: str) -> None:
        """Parses INI content from string."""
        self._config.read_string(ini_text)

    def load_ini_file(self, filepath: str) -> None:
        """Loads INI file from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Config file not found: {filepath}")
        self._config.read(filepath, encoding="utf-8")

    def apply_env_overrides(self, prefix: str = "APP_") -> None:
        """
        Scans os.environ for variables matching prefix.
        Splits pattern PREFIX_{SECTION}_{KEY} and registers overrides.
        E.g., APP_SERVER_PORT=9000 maps to section 'server', key 'port'.
        """
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                remainder = env_key[len(prefix):]
                parts = remainder.split("_", 1)
                if len(parts) == 2:
                    section = parts[0].lower()
                    key = parts[1].lower()
                    if section not in self._env_overrides:
                        self._env_overrides[section] = {}
                    self._env_overrides[section][key] = env_val

    def _get_raw(self, section: str, key: str, fallback: Optional[Any] = None) -> str:
        """Resolves value following precedence: Env Var > INI Config > Fallback."""
        sec_lower = section.lower()
        key_lower = key.lower()

        # 1. Check environment overrides
        if sec_lower in self._env_overrides and key_lower in self._env_overrides[sec_lower]:
            return self._env_overrides[sec_lower][key_lower]

        # 2. Check INI config
        if self._config.has_section(sec_lower) and self._config.has_option(sec_lower, key_lower):
            return self._config.get(sec_lower, key_lower)

        # 3. Check fallback
        if fallback is not None:
            return str(fallback)

        raise ConfigMissingError(f"Missing required configuration: [{section}] -> '{key}'")

    def get_string(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """Fetches string value."""
        return self._get_raw(section, key, fallback=fallback)

    def get_int(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        """Fetches integer value with strict conversion."""
        raw = self._get_raw(section, key, fallback=fallback)
        try:
            return int(raw)
        except ValueError as err:
            raise ValueError(f"Configuration [{section}] '{key}' value '{raw}' is not an integer") from err

    def get_float(self, section: str, key: str, fallback: Optional[float] = None) -> float:
        """Fetches float value with strict conversion."""
        raw = self._get_raw(section, key, fallback=fallback)
        try:
            return float(raw)
        except ValueError as err:
            raise ValueError(f"Configuration [{section}] '{key}' value '{raw}' is not a float") from err

    def get_bool(self, section: str, key: str, fallback: Optional[bool] = None) -> bool:
        """Fetches boolean value supporting true/false, yes/no, 1/0."""
        raw = self._get_raw(section, key, fallback=fallback).strip().lower()
        if raw in ("true", "yes", "1", "on"):
            return True
        elif raw in ("false", "no", "0", "off"):
            return False
        raise ValueError(f"Configuration [{section}] '{key}' value '{raw}' is not a valid boolean")

    def to_dict(self) -> Dict[str, Dict[str, str]]:
        """Compiles merged dictionary including env overrides."""
        merged: Dict[str, Dict[str, str]] = {}

        # Base config
        for sec in self._config.sections():
            merged[sec] = dict(self._config.items(sec))

        # Apply env overrides
        for sec, keys in self._env_overrides.items():
            if sec not in merged:
                merged[sec] = {}
            for k, v in keys.items():
                merged[sec][k] = v

        return merged

    def export_to_json(self, filepath: str) -> None:
        """Exports merged config to structured JSON file."""
        merged_dict = self.to_dict()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(merged_dict, f, indent=2)


if __name__ == "__main__":
    ini_text = """
[server]
host = 127.0.0.1
port = 8080
debug = true
workers = 4

[database]
engine = sqlite
name = app_production.db
pool_size = 10
timeout = 30.5
"""
    # Simulate environment override
    os.environ["APP_SERVER_PORT"] = "9000"

    manager = ConfigManager()
    manager.load_ini_string(ini_text)
    manager.apply_env_overrides(prefix="APP_")

    print("=== 1. Strongly-Typed Getters & Precedence Resolution ===")
    srv_host = manager.get_string("server", "host")
    srv_port = manager.get_int("server", "port")  # Overridden by environment
    is_debug = manager.get_bool("server", "debug")
    db_timeout = manager.get_float("database", "timeout")

    print(f"Server Host: '{srv_host}'")
    print(f"Server Port (Env Overridden): {srv_port}")
    print(f"Server Debug Mode: {is_debug}")
    print(f"Database Timeout: {db_timeout}")

    print("\n=== 2. Fallback Resolution ===")
    missing_with_fallback = manager.get_string("server", "tls_cert", fallback="/etc/ssl/cert.pem")
    print(f"TLS Cert with fallback: '{missing_with_fallback}'")

    print("\n=== 3. Missing Key Exception Validation ===")
    try:
        manager.get_string("security", "jwt_secret")
    except ConfigMissingError as err:
        print(f"Caught expected ConfigMissingError:\n  {err}")

    print("\n=== 4. JSON Export Verification ===")
    merged = manager.to_dict()
    print("Merged Config Exported to JSON Preview:")
    print(json.dumps(merged, indent=2))
