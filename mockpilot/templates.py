"""
Template Manager - Built-in API templates for common scenarios
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional


class TemplateManager:
    """Manage built-in and custom mock templates"""
    
    # Built-in templates for common API scenarios
    BUILT_IN_TEMPLATES: Dict[str, Dict[str, Any]] = {
        "rest-api": {
            "name": "REST API",
            "description": "Standard RESTful API with CRUD operations",
            "routes": [
                {
                    "path": "/api/resources",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "data": [
                            {"id": 1, "name": "Resource 1", "status": "active"},
                            {"id": 2, "name": "Resource 2", "status": "inactive"}
                        ],
                        "meta": {"total": 2, "page": 1, "per_page": 10}
                    }
                },
                {
                    "path": "/api/resources/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "name": "Resource 1",
                        "description": "A sample resource",
                        "status": "active",
                        "created_at": "2025-01-01T00:00:00Z"
                    }
                },
                {
                    "path": "/api/resources",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "id": 3,
                        "name": "New Resource",
                        "message": "Resource created successfully"
                    }
                },
                {
                    "path": "/api/resources/{id}",
                    "method": "PUT",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "message": "Resource updated successfully"
                    }
                },
                {
                    "path": "/api/resources/{id}",
                    "method": "DELETE",
                    "status": 204,
                    "response": {}
                }
            ]
        },
        
        "auth-api": {
            "name": "Authentication API",
            "description": "User authentication and authorization endpoints",
            "routes": [
                {
                    "path": "/api/auth/login",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "Bearer",
                        "expires_in": 3600,
                        "user": {
                            "id": 1,
                            "email": "user@example.com",
                            "name": "John Doe"
                        }
                    }
                },
                {
                    "path": "/api/auth/register",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "id": 2,
                        "email": "newuser@example.com",
                        "message": "User registered successfully"
                    }
                },
                {
                    "path": "/api/auth/refresh",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "Bearer",
                        "expires_in": 3600
                    }
                },
                {
                    "path": "/api/auth/logout",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "message": "Logged out successfully"
                    }
                },
                {
                    "path": "/api/auth/me",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "email": "user@example.com",
                        "name": "John Doe",
                        "avatar": "https://example.com/avatar.jpg",
                        "role": "user"
                    }
                }
            ]
        },
        
        "ecommerce": {
            "name": "E-commerce API",
            "description": "Online store API with products, cart, and orders",
            "routes": [
                {
                    "path": "/api/products",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "products": [
                            {
                                "id": 1,
                                "name": "Wireless Headphones",
                                "price": 99.99,
                                "category": "Electronics",
                                "in_stock": True
                            },
                            {
                                "id": 2,
                                "name": "Smart Watch",
                                "price": 249.99,
                                "category": "Electronics",
                                "in_stock": True
                            }
                        ],
                        "total": 2
                    }
                },
                {
                    "path": "/api/products/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "name": "Wireless Headphones",
                        "description": "High-quality wireless headphones with noise cancellation",
                        "price": 99.99,
                        "category": "Electronics",
                        "images": ["https://example.com/img1.jpg"],
                        "in_stock": True,
                        "rating": 4.5
                    }
                },
                {
                    "path": "/api/cart",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "items": [
                            {"product_id": 1, "quantity": 2, "price": 99.99}
                        ],
                        "total": 199.98
                    }
                },
                {
                    "path": "/api/cart/items",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "message": "Item added to cart",
                        "cart_id": "cart_123"
                    }
                },
                {
                    "path": "/api/orders",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "order_id": "ORD-2025-001",
                        "status": "pending",
                        "total": 199.98,
                        "message": "Order placed successfully"
                    }
                },
                {
                    "path": "/api/orders/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "order_id": "ORD-2025-001",
                        "status": "shipped",
                        "items": [
                            {"product_id": 1, "name": "Wireless Headphones", "quantity": 2}
                        ],
                        "total": 199.98,
                        "shipping_address": {
                            "street": "123 Main St",
                            "city": "New York",
                            "zip": "10001"
                        }
                    }
                }
            ]
        },
        
        "social-media": {
            "name": "Social Media API",
            "description": "Social platform API with posts, comments, and likes",
            "routes": [
                {
                    "path": "/api/posts",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "posts": [
                            {
                                "id": 1,
                                "author": {"id": 1, "name": "Alice", "avatar": "..."},
                                "content": "Hello, world!",
                                "likes": 42,
                                "comments_count": 5,
                                "created_at": "2025-01-15T10:30:00Z"
                            },
                            {
                                "id": 2,
                                "author": {"id": 2, "name": "Bob", "avatar": "..."},
                                "content": "Beautiful day!",
                                "likes": 28,
                                "comments_count": 3,
                                "created_at": "2025-01-15T09:00:00Z"
                            }
                        ]
                    }
                },
                {
                    "path": "/api/posts/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "id": 1,
                        "author": {"id": 1, "name": "Alice", "avatar": "..."},
                        "content": "Hello, world!",
                        "likes": 42,
                        "comments": [
                            {"id": 1, "author": "Bob", "content": "Great post!"}
                        ],
                        "created_at": "2025-01-15T10:30:00Z"
                    }
                },
                {
                    "path": "/api/posts",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "id": 3,
                        "message": "Post created successfully"
                    }
                },
                {
                    "path": "/api/posts/{id}/like",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "likes": 43,
                        "message": "Post liked"
                    }
                },
                {
                    "path": "/api/posts/{id}/comments",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "comments": [
                            {"id": 1, "author": "Bob", "content": "Great post!", "created_at": "2025-01-15T11:00:00Z"}
                        ]
                    }
                }
            ]
        },
        
        "weather": {
            "name": "Weather API",
            "description": "Weather data API with current conditions and forecasts",
            "routes": [
                {
                    "path": "/api/weather/current",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "location": {
                            "city": "Beijing",
                            "country": "CN",
                            "lat": 39.9042,
                            "lon": 116.4074
                        },
                        "current": {
                            "temperature": 22,
                            "feels_like": 21,
                            "humidity": 45,
                            "pressure": 1013,
                            "wind_speed": 3.5,
                            "wind_direction": "NE",
                            "condition": "Partly Cloudy",
                            "icon": "partly-cloudy-day"
                        },
                        "updated_at": "2025-01-15T12:00:00Z"
                    }
                },
                {
                    "path": "/api/weather/forecast",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "location": {"city": "Beijing", "country": "CN"},
                        "forecast": [
                            {
                                "date": "2025-01-16",
                                "high": 24,
                                "low": 15,
                                "condition": "Sunny",
                                "precipitation": 0
                            },
                            {
                                "date": "2025-01-17",
                                "high": 22,
                                "low": 14,
                                "condition": "Cloudy",
                                "precipitation": 10
                            }
                        ]
                    }
                }
            ]
        },
        
        "health-check": {
            "name": "Health Check",
            "description": "Simple health check and status endpoints",
            "routes": [
                {
                    "path": "/health",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "status": "healthy",
                        "timestamp": "2025-01-15T12:00:00Z",
                        "uptime": "3d 2h 15m"
                    }
                },
                {
                    "path": "/ready",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "ready": True,
                        "checks": {
                            "database": "connected",
                            "cache": "connected"
                        }
                    }
                },
                {
                    "path": "/metrics",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "requests_total": 15234,
                        "requests_per_second": 45.2,
                        "average_response_time_ms": 23,
                        "error_rate": 0.001
                    }
                }
            ]
        },
        
        "error-simulation": {
            "name": "Error Simulation",
            "description": "Endpoints that simulate various error scenarios",
            "routes": [
                {
                    "path": "/api/errors/400",
                    "method": "GET",
                    "status": 400,
                    "response": {
                        "error": "Bad Request",
                        "message": "Invalid parameters provided",
                        "details": {"field": "email", "issue": "Invalid format"}
                    }
                },
                {
                    "path": "/api/errors/401",
                    "method": "GET",
                    "status": 401,
                    "response": {
                        "error": "Unauthorized",
                        "message": "Authentication required"
                    }
                },
                {
                    "path": "/api/errors/403",
                    "method": "GET",
                    "status": 403,
                    "response": {
                        "error": "Forbidden",
                        "message": "You don't have permission to access this resource"
                    }
                },
                {
                    "path": "/api/errors/404",
                    "method": "GET",
                    "status": 404,
                    "response": {
                        "error": "Not Found",
                        "message": "The requested resource was not found"
                    }
                },
                {
                    "path": "/api/errors/500",
                    "method": "GET",
                    "status": 500,
                    "response": {
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred"
                    }
                },
                {
                    "path": "/api/errors/503",
                    "method": "GET",
                    "status": 503,
                    "response": {
                        "error": "Service Unavailable",
                        "message": "Service temporarily unavailable",
                        "retry_after": 30
                    }
                }
            ]
        },
        
        "pagination": {
            "name": "Pagination Example",
            "description": "Demonstrates pagination patterns",
            "routes": [
                {
                    "path": "/api/items",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "data": [
                            {"id": 1, "name": "Item 1"},
                            {"id": 2, "name": "Item 2"},
                            {"id": 3, "name": "Item 3"}
                        ],
                        "pagination": {
                            "page": 1,
                            "per_page": 10,
                            "total": 100,
                            "total_pages": 10,
                            "has_next": True,
                            "has_prev": False
                        },
                        "links": {
                            "self": "/api/items?page=1",
                            "next": "/api/items?page=2",
                            "last": "/api/items?page=10"
                        }
                    }
                }
            ]
        },
        
        "webhook": {
            "name": "Webhook Receiver",
            "description": "Endpoints for testing webhook integrations",
            "routes": [
                {
                    "path": "/webhooks/receive",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "received": True,
                        "webhook_id": "wh_123456",
                        "processed_at": "2025-01-15T12:00:00Z"
                    }
                },
                {
                    "path": "/webhooks/events",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "events": [
                            {
                                "id": "evt_1",
                                "type": "payment.succeeded",
                                "created_at": "2025-01-15T11:00:00Z",
                                "data": {"amount": 99.99, "currency": "USD"}
                            }
                        ]
                    }
                }
            ]
        },
        
        "graphql": {
            "name": "GraphQL Mock",
            "description": "Simple GraphQL endpoint mock",
            "routes": [
                {
                    "path": "/graphql",
                    "method": "POST",
                    "status": 200,
                    "response": {
                        "data": {
                            "user": {
                                "id": "1",
                                "name": "John Doe",
                                "email": "john@example.com"
                            }
                        }
                    }
                },
                {
                    "path": "/graphql",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "data": None,
                        "errors": [{"message": "GraphQL queries must be POST requests"}]
                    }
                }
            ]
        },
        
        "file-upload": {
            "name": "File Upload",
            "description": "File upload and download endpoints",
            "routes": [
                {
                    "path": "/api/upload",
                    "method": "POST",
                    "status": 201,
                    "response": {
                        "file_id": "file_123",
                        "filename": "document.pdf",
                        "size": 1024000,
                        "mime_type": "application/pdf",
                        "uploaded_at": "2025-01-15T12:00:00Z",
                        "url": "/api/files/file_123"
                    }
                },
                {
                    "path": "/api/files/{id}",
                    "method": "GET",
                    "status": 200,
                    "response": {
                        "file_id": "file_123",
                        "filename": "document.pdf",
                        "size": 1024000,
                        "mime_type": "application/pdf",
                        "download_url": "/api/files/file_123/download"
                    }
                },
                {
                    "path": "/api/files/{id}",
                    "method": "DELETE",
                    "status": 204,
                    "response": {}
                }
            ]
        }
    }
    
    def __init__(self, templates_dir: Optional[str] = None):
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self.custom_templates: Dict[str, Dict[str, Any]] = {}
        
        if self.templates_dir and self.templates_dir.exists():
            self._load_custom_templates()
    
    def _load_custom_templates(self) -> None:
        """Load custom templates from directory"""
        if not self.templates_dir:
            return
        
        for template_file in self.templates_dir.glob("*.json"):
            try:
                with open(template_file, "r", encoding="utf-8") as f:
                    template = json.load(f)
                    template_name = template_file.stem
                    self.custom_templates[template_name] = template
            except Exception:
                pass
    
    def list_templates(self) -> List[Dict[str, str]]:
        """List all available templates"""
        templates = []
        
        # Built-in templates
        for key, template in self.BUILT_IN_TEMPLATES.items():
            templates.append({
                "name": key,
                "display_name": template.get("name", key),
                "description": template.get("description", ""),
                "type": "built-in",
                "route_count": len(template.get("routes", []))
            })
        
        # Custom templates
        for key, template in self.custom_templates.items():
            templates.append({
                "name": key,
                "display_name": template.get("name", key),
                "description": template.get("description", ""),
                "type": "custom",
                "route_count": len(template.get("routes", []))
            })
        
        return templates
    
    def get_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a template by name"""
        if name in self.BUILT_IN_TEMPLATES:
            return self.BUILT_IN_TEMPLATES[name].copy()
        if name in self.custom_templates:
            return self.custom_templates[name].copy()
        return None
    
    def get_template_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get full configuration for a template"""
        template = self.get_template(name)
        if not template:
            return None
        
        return {
            "server": {"host": "localhost", "port": 8080},
            "settings": {"cors": True, "delay": 0, "recording": False},
            "routes": template.get("routes", [])
        }
    
    def save_template(self, name: str, template: Dict[str, Any]) -> bool:
        """Save a custom template"""
        if not self.templates_dir:
            return False
        
        try:
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            template_file = self.templates_dir / f"{name}.json"
            
            with open(template_file, "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2, ensure_ascii=False)
            
            self.custom_templates[name] = template
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_categories() -> List[Dict[str, Any]]:
        """Get template categories"""
        return [
            {"id": "api", "name": "API Types", "templates": ["rest-api", "auth-api", "graphql"]},
            {"id": "domain", "name": "Business Domains", "templates": ["ecommerce", "social-media", "weather"]},
            {"id": "utility", "name": "Utilities", "templates": ["health-check", "webhook", "file-upload"]},
            {"id": "testing", "name": "Testing", "templates": ["error-simulation", "pagination"]}
        ]
