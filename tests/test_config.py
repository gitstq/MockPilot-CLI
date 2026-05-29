"""
Tests for configuration loader
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from mockpilot.config import ConfigLoader


class TestConfigLoader(unittest.TestCase):
    """Test configuration loader"""
    
    def setUp(self):
        self.loader = ConfigLoader()
    
    def test_load_json_config(self):
        """Test loading JSON configuration"""
        config = {
            "server": {"host": "localhost", "port": 8080},
            "routes": [
                {"path": "/test", "method": "GET", "response": {"message": "ok"}}
            ]
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            loaded = self.loader.load(temp_path)
            self.assertEqual(loaded["server"]["port"], 8080)
            self.assertEqual(len(loaded["routes"]), 1)
        finally:
            os.unlink(temp_path)
    
    def test_load_yaml_config(self):
        """Test loading YAML configuration"""
        yaml_content = """
server:
  host: localhost
  port: 9090
routes:
  - path: /api/users
    method: GET
    response:
      users: []
"""
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            temp_path = f.name
        
        try:
            loaded = self.loader.load(temp_path)
            self.assertEqual(loaded["server"]["port"], 9090)
        finally:
            os.unlink(temp_path)
    
    def test_validate_missing_routes(self):
        """Test validation fails without routes"""
        config = {"server": {"host": "localhost"}}
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.loader.load(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_validate_missing_path(self):
        """Test validation fails without path in route"""
        config = {
            "routes": [{"method": "GET", "response": {}}]
        }
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f)
            temp_path = f.name
        
        try:
            with self.assertRaises(ValueError):
                self.loader.load(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_get_routes_by_method(self):
        """Test getting routes organized by method"""
        self.loader.config = {
            "routes": [
                {"path": "/users", "method": "GET"},
                {"path": "/users", "method": "POST"},
                {"path": "/users/1", "method": "DELETE"}
            ]
        }
        
        routes = self.loader.get_routes()
        self.assertEqual(len(routes["GET"]), 1)
        self.assertEqual(len(routes["POST"]), 1)
        self.assertEqual(len(routes["DELETE"]), 1)
    
    def test_create_sample_config(self):
        """Test sample config creation"""
        config = ConfigLoader.create_sample_config()
        self.assertIn("server", config)
        self.assertIn("routes", config)
        self.assertGreater(len(config["routes"]), 0)


if __name__ == "__main__":
    unittest.main()
