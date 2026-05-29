"""
Configuration Loader - Load and validate mock configurations
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union


class ConfigLoader:
    """Load and validate mock server configuration"""
    
    # Supported HTTP methods
    SUPPORTED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
    
    def load(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file"""
        config_path = path or self.config_path
        
        if not config_path:
            raise ValueError("Configuration path not provided")
        
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Determine file type from extension
        suffix = config_file.suffix.lower()
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            if suffix == ".json":
                self.config = json.loads(content)
            elif suffix in [".yaml", ".yml"]:
                self.config = self._parse_yaml(content)
            else:
                # Try JSON first, then YAML
                try:
                    self.config = json.loads(content)
                except json.JSONDecodeError:
                    self.config = self._parse_yaml(content)
        
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {e}")
        
        # Validate configuration
        self._validate()
        
        return self.config
    
    def _parse_yaml(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for basic configurations"""
        lines = content.split("\n")
        return self._parse_yaml_block(lines, 0, 0)[0]
    
    def _parse_yaml_block(self, lines: List[str], start: int, base_indent: int) -> tuple:
        """Parse a block of YAML, return (result, next_line_index)"""
        result: Dict[str, Any] = {}
        i = start
        current_list: Optional[List[Any]] = None
        current_list_key: Optional[str] = None
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                i += 1
                continue
            
            # Calculate indent level
            indent = len(line) - len(line.lstrip())
            
            # If we've de-indented past base level, return to parent
            if indent < base_indent:
                break
            
            # Handle list items at base level
            if indent == base_indent and stripped.startswith("- "):
                if current_list is None:
                    # This shouldn't happen at root level
                    i += 1
                    continue
                
                value = stripped[2:].strip()
                
                # Check if this is a nested object in a list
                if ":" in value:
                    key, val = value.split(":", 1)
                    key = key.strip()
                    val = val.strip()
                    
                    if not current_list or not isinstance(current_list[-1], dict):
                        current_list.append({})
                    
                    if val == "":
                        # Nested structure in list item
                        nested_obj, i = self._parse_yaml_block(lines, i + 1, indent + 2)
                        current_list[-1][key] = nested_obj
                        continue
                    else:
                        current_list[-1][key] = self._parse_yaml_value(val)
                else:
                    # Check for nested structure
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        next_stripped = next_line.strip()
                        if next_stripped and not next_stripped.startswith("#"):
                            next_indent = len(next_line) - len(next_line.lstrip())
                            if next_indent > indent:
                                nested_obj, i = self._parse_yaml_block(lines, i + 1, next_indent)
                                current_list.append(nested_obj)
                                continue
                    
                    current_list.append(self._parse_yaml_value(value))
            
            # Handle key-value pairs
            elif ":" in stripped:
                key, val = stripped.split(":", 1)
                key = key.strip()
                val = val.strip()
                
                if val == "":
                    # This is a nested structure
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        next_stripped = next_line.strip()
                        if next_stripped and not next_stripped.startswith("#"):
                            next_indent = len(next_line) - len(next_line.lstrip())
                            if next_indent > indent:
                                # Check if it's a list
                                if next_stripped.startswith("-"):
                                    result[key] = []
                                    current_list = result[key]
                                    current_list_key = key
                                    i += 1
                                    continue
                                else:
                                    # Nested object
                                    nested_obj, i = self._parse_yaml_block(lines, i + 1, next_indent)
                                    result[key] = nested_obj
                                    continue
                    
                    result[key] = None
                else:
                    result[key] = self._parse_yaml_value(val)
            
            i += 1
        
        return result, i
    
    def _parse_yaml_value(self, value: str) -> Any:
        """Parse a YAML value to appropriate Python type"""
        value = value.strip()
        
        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Handle booleans
        if value.lower() in ("true", "yes", "on"):
            return True
        if value.lower() in ("false", "no", "off"):
            return False
        
        # Handle null
        if value.lower() in ("null", "none", "~"):
            return None
        
        # Handle numbers
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        return value
    
    def _validate(self) -> None:
        """Validate configuration structure"""
        if not isinstance(self.config, dict):
            raise ValueError("Configuration must be a dictionary")
        
        # Check for required fields
        if "routes" not in self.config:
            raise ValueError("Configuration must contain 'routes' section")
        
        routes = self.config.get("routes", [])
        if not isinstance(routes, list):
            raise ValueError("'routes' must be a list")
        
        for i, route in enumerate(routes):
            self._validate_route(route, i)
    
    def _validate_route(self, route: Dict[str, Any], index: int) -> None:
        """Validate a single route configuration"""
        if not isinstance(route, dict):
            raise ValueError(f"Route {index} must be a dictionary")
        
        # Check required fields
        if "path" not in route:
            raise ValueError(f"Route {index} must have a 'path' field")
        
        # Validate method
        method = route.get("method", "GET").upper()
        if method not in self.SUPPORTED_METHODS:
            raise ValueError(f"Route {index}: Unsupported method '{method}'")
        
        # Validate path
        path = route.get("path", "")
        if not path or not isinstance(path, str):
            raise ValueError(f"Route {index}: 'path' must be a non-empty string")
    
    def get_routes(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get routes organized by HTTP method"""
        routes_by_method: Dict[str, List[Dict[str, Any]]] = {}
        
        for method in self.SUPPORTED_METHODS:
            routes_by_method[method] = []
        
        routes = self.config.get("routes", [])
        for route in routes:
            method = route.get("method", "GET").upper()
            if method in routes_by_method:
                routes_by_method[method].append(route)
        
        return routes_by_method
    
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration"""
        return self.config.get("server", {})
    
    def get_settings(self) -> Dict[str, Any]:
        """Get general settings"""
        return self.config.get("settings", {})
    
    @staticmethod
    def create_sample_config() -> Dict[str, Any]:
        """Create a sample configuration"""
        return {
            "server": {
                "host": "localhost",
                "port": 8080
            },
            "settings": {
                "cors": True,
                "delay": 0,
                "recording": False
            },
            "routes": [
                {
                    "path": "/api/users",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "users": [
                            {"id": 1, "name": "Alice"},
                            {"id": 2, "name": "Bob"}
                        ]
                    }
                },
                {
                    "path": "/api/users/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "name": "Alice",
                        "email": "alice@example.com"
                    }
                },
                {
                    "path": "/api/users",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "id": 3,
                        "message": "User created successfully"
                    }
                }
            ]
        }
