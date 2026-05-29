"""
Tests for template manager
"""

import unittest
from mockpilot.templates import TemplateManager


class TestTemplateManager(unittest.TestCase):
    """Test template manager"""
    
    def setUp(self):
        self.manager = TemplateManager()
    
    def test_list_templates(self):
        """Test listing templates"""
        templates = self.manager.list_templates()
        self.assertGreater(len(templates), 0)
        
        # Check template structure
        for template in templates:
            self.assertIn("name", template)
            self.assertIn("display_name", template)
            self.assertIn("type", template)
    
    def test_get_template(self):
        """Test getting a template"""
        template = self.manager.get_template("rest-api")
        self.assertIsNotNone(template)
        self.assertIn("routes", template)
        self.assertIn("name", template)
    
    def test_get_nonexistent_template(self):
        """Test getting non-existent template"""
        template = self.manager.get_template("nonexistent")
        self.assertIsNone(template)
    
    def test_get_template_config(self):
        """Test getting full template configuration"""
        config = self.manager.get_template_config("health-check")
        self.assertIsNotNone(config)
        self.assertIn("server", config)
        self.assertIn("settings", config)
        self.assertIn("routes", config)
    
    def test_get_categories(self):
        """Test getting template categories"""
        categories = TemplateManager.get_categories()
        self.assertGreater(len(categories), 0)
        
        for category in categories:
            self.assertIn("id", category)
            self.assertIn("name", category)
            self.assertIn("templates", category)
    
    def test_built_in_templates_exist(self):
        """Test that all built-in templates exist"""
        expected_templates = [
            "rest-api",
            "auth-api",
            "ecommerce",
            "health-check",
            "error-simulation"
        ]
        
        for template_name in expected_templates:
            template = self.manager.get_template(template_name)
            self.assertIsNotNone(template, f"Template {template_name} should exist")


if __name__ == "__main__":
    unittest.main()
