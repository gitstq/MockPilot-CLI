"""
Mock Server Core - HTTP server implementation for API mocking
"""

import json
import re
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Dict, Any, Optional, Callable, List
import threading


class MockHandler(BaseHTTPRequestHandler):
    """HTTP request handler for mock server"""
    
    # Class-level storage for routes and recordings
    routes: Dict[str, List[Dict[str, Any]]] = {}
    recordings: List[Dict[str, Any]] = []
    enable_recording: bool = False
    delay: float = 0
    cors_enabled: bool = True
    
    def log_message(self, format: str, *args) -> None:
        """Suppress default logging"""
        pass
    
    def _send_cors_headers(self) -> None:
        """Send CORS headers if enabled"""
        if self.cors_enabled:
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    def _match_route(self, method: str, path: str) -> Optional[Dict[str, Any]]:
        """Find matching route for request"""
        method_routes = self.routes.get(method.upper(), [])
        
        for route in method_routes:
            pattern = route.get("path_pattern", route.get("path", ""))
            
            # Convert path pattern to regex
            if "{" in pattern:
                # Handle path parameters like /users/{id}
                regex_pattern = re.sub(r"\{([^}]+)\}", r"(?P<\1>[^/]+)", pattern)
                regex_pattern = f"^{regex_pattern}$"
                match = re.match(regex_pattern, path)
                if match:
                    route_copy = route.copy()
                    route_copy["path_params"] = match.groupdict()
                    return route_copy
            else:
                # Exact match or wildcard
                if pattern == path or pattern == "*":
                    return route
                # Support * wildcard at end
                if pattern.endswith("*"):
                    prefix = pattern[:-1]
                    if path.startswith(prefix):
                        return route
        
        return None
    
    def _parse_request_body(self) -> Optional[Any]:
        """Parse request body based on content type"""
        content_length = self.headers.get("Content-Length")
        if not content_length:
            return None
        
        try:
            length = int(content_length)
            body = self.rfile.read(length).decode("utf-8")
            
            content_type = self.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return json.loads(body)
            elif "application/x-www-form-urlencoded" in content_type:
                return parse_qs(body)
            else:
                return body
        except Exception:
            return None
    
    def _record_request(self, method: str, path: str, request_body: Any, 
                       response_status: int, response_body: Any) -> None:
        """Record request/response pair"""
        if self.enable_recording:
            self.recordings.append({
                "timestamp": time.time(),
                "method": method,
                "path": path,
                "request_body": request_body,
                "response_status": response_status,
                "response_body": response_body
            })
    
    def _handle_request(self, method: str) -> None:
        """Handle HTTP request"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_string = parsed_path.query
        query_params = parse_qs(query_string) if query_string else {}
        
        # Simulate delay if configured
        if self.delay > 0:
            time.sleep(self.delay)
        
        # Find matching route
        route = self._match_route(method, path)
        
        if not route:
            # Return 404
            self.send_response(404)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": "Not Found", "path": path, "method": method}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))
            return
        
        # Parse request body
        request_body = self._parse_request_body()
        
        # Get response configuration
        response_status = route.get("status", 200)
        response_body = route.get("response", {})
        response_headers = route.get("headers", {})
        
        # Handle dynamic response
        if callable(response_body):
            try:
                context = {
                    "method": method,
                    "path": path,
                    "query": query_params,
                    "body": request_body,
                    "path_params": route.get("path_params", {}),
                    "headers": dict(self.headers)
                }
                response_body = response_body(context)
            except Exception as e:
                response_status = 500
                response_body = {"error": str(e)}
        
        # Send response
        self.send_response(response_status)
        self._send_cors_headers()
        
        # Set content type
        content_type = response_headers.get("Content-Type", "application/json")
        self.send_header("Content-Type", content_type)
        
        # Add custom headers
        for header, value in response_headers.items():
            if header.lower() != "content-type":
                self.send_header(header, value)
        
        self.end_headers()
        
        # Write response body
        if isinstance(response_body, (dict, list)):
            self.wfile.write(json.dumps(response_body).encode("utf-8"))
        elif isinstance(response_body, str):
            self.wfile.write(response_body.encode("utf-8"))
        else:
            self.wfile.write(str(response_body).encode("utf-8"))
        
        # Record the interaction
        self._record_request(method, path, request_body, response_status, response_body)
    
    def do_GET(self) -> None:
        self._handle_request("GET")
    
    def do_POST(self) -> None:
        self._handle_request("POST")
    
    def do_PUT(self) -> None:
        self._handle_request("PUT")
    
    def do_DELETE(self) -> None:
        self._handle_request("DELETE")
    
    def do_PATCH(self) -> None:
        self._handle_request("PATCH")
    
    def do_OPTIONS(self) -> None:
        """Handle CORS preflight requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()


class MockServer:
    """Mock HTTP Server"""
    
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
    
    def set_routes(self, routes: Dict[str, List[Dict[str, Any]]]) -> None:
        """Set routes for the mock server"""
        MockHandler.routes = routes
    
    def set_recording(self, enabled: bool) -> None:
        """Enable/disable request recording"""
        MockHandler.enable_recording = enabled
    
    def set_delay(self, delay: float) -> None:
        """Set artificial delay for responses (in seconds)"""
        MockHandler.delay = delay
    
    def set_cors(self, enabled: bool) -> None:
        """Enable/disable CORS headers"""
        MockHandler.cors_enabled = enabled
    
    def get_recordings(self) -> List[Dict[str, Any]]:
        """Get recorded requests"""
        return MockHandler.recordings.copy()
    
    def clear_recordings(self) -> None:
        """Clear recorded requests"""
        MockHandler.recordings.clear()
    
    def start(self, blocking: bool = False) -> None:
        """Start the mock server"""
        if self.is_running:
            return
        
        self.server = HTTPServer((self.host, self.port), MockHandler)
        self.is_running = True
        
        if blocking:
            print(f"🚀 MockPilot server running at http://{self.host}:{self.port}")
            print("Press Ctrl+C to stop")
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                self.stop()
        else:
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
    
    def stop(self) -> None:
        """Stop the mock server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.is_running = False
            print("\n✅ MockPilot server stopped")
