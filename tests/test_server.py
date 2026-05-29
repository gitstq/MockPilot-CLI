"""
Tests for mock server
"""

import json
import threading
import time
import unittest
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from mockpilot.server import MockServer


class TestMockServer(unittest.TestCase):
    """Test mock server"""
    
    def setUp(self):
        self.server = MockServer(host="localhost", port=8765)
        self.base_url = "http://localhost:8765"
    
    def tearDown(self):
        if self.server.is_running:
            self.server.stop()
    
    def test_server_start_stop(self):
        """Test starting and stopping server"""
        self.assertFalse(self.server.is_running)
        
        self.server.start(blocking=False)
        self.assertTrue(self.server.is_running)
        
        self.server.stop()
        self.assertFalse(self.server.is_running)
    
    def test_basic_route(self):
        """Test basic route handling"""
        routes = {
            "GET": [
                {
                    "path": "/test",
                    "response": {"message": "hello"}
                }
            ]
        }
        
        self.server.set_routes(routes)
        self.server.start(blocking=False)
        time.sleep(0.1)  # Wait for server to start
        
        try:
            response = urlopen(f"{self.base_url}/test")
            data = json.loads(response.read().decode())
            self.assertEqual(data["message"], "hello")
        finally:
            self.server.stop()
    
    def test_404_response(self):
        """Test 404 for non-existent route"""
        routes = {"GET": []}
        
        self.server.set_routes(routes)
        self.server.start(blocking=False)
        time.sleep(0.1)
        
        try:
            with self.assertRaises(HTTPError) as context:
                urlopen(f"{self.base_url}/nonexistent")
            self.assertEqual(context.exception.code, 404)
        finally:
            self.server.stop()
    
    def test_path_parameters(self):
        """Test path parameter extraction"""
        routes = {
            "GET": [
                {
                    "path": "/users/{id}",
                    "response": {"user_id": "dynamic"}
                }
            ]
        }
        
        self.server.set_routes(routes)
        self.server.start(blocking=False)
        time.sleep(0.1)
        
        try:
            response = urlopen(f"{self.base_url}/users/123")
            data = json.loads(response.read().decode())
            self.assertEqual(data["user_id"], "dynamic")
        finally:
            self.server.stop()
    
    def test_recording(self):
        """Test request recording"""
        routes = {
            "GET": [
                {"path": "/record-test", "response": {"test": True}}
            ]
        }
        
        self.server.set_routes(routes)
        self.server.set_recording(True)
        self.server.start(blocking=False)
        time.sleep(0.1)
        
        try:
            urlopen(f"{self.base_url}/record-test")
            
            recordings = self.server.get_recordings()
            self.assertEqual(len(recordings), 1)
            self.assertEqual(recordings[0]["method"], "GET")
            self.assertEqual(recordings[0]["path"], "/record-test")
        finally:
            self.server.stop()
    
    def test_cors_headers(self):
        """Test CORS headers"""
        routes = {
            "GET": [
                {"path": "/cors-test", "response": {}}
            ]
        }
        
        self.server.set_routes(routes)
        self.server.set_cors(True)
        self.server.start(blocking=False)
        time.sleep(0.1)
        
        try:
            request = Request(f"{self.base_url}/cors-test", method="OPTIONS")
            request.add_header("Origin", "http://example.com")
            response = urlopen(request)
            
            self.assertIn("access-control-allow-origin", 
                         [h[0].lower() for h in response.getheaders()])
        finally:
            self.server.stop()


if __name__ == "__main__":
    unittest.main()
