# WhatsApp Group Link Scraper API

## Overview

This is a Flask-based web API that extracts metadata from WhatsApp group invite links. The application scrapes Open Graph tags (title, image) from WhatsApp group URLs using rotating proxy configurations to avoid rate limiting and IP blocking. It provides a RESTful API interface with comprehensive documentation and a web-based testing interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Lightweight Python web framework chosen for its simplicity and flexibility
- **CORS enabled**: Allows cross-origin requests for frontend integration
- **Environment-based configuration**: Uses environment variables for sensitive data like proxy credentials

### Web Scraping Architecture
- **BeautifulSoup**: HTML parsing library for extracting Open Graph meta tags
- **Requests library**: HTTP client with proxy support for making web requests
- **Rotating proxy system**: Implements proxy rotation to avoid IP blocking and rate limits
- **Retry mechanism**: Built-in retry logic with configurable max attempts

### Proxy Management
- **Dynamic proxy configuration**: Supports configurable proxy pools with IP ranges
- **SOCKS5 protocol**: Uses SOCKS5 proxies for better anonymity and performance
- **Random proxy selection**: Randomly selects from available proxy pool for each request
- **Authentication support**: Handles username/password authentication for proxy services

### Error Handling and Validation
- **WhatsApp URL validation**: Validates input URLs to ensure they're valid WhatsApp group links
- **Comprehensive error responses**: Returns structured JSON error messages with appropriate HTTP status codes
- **Request timeout handling**: Configurable timeouts to prevent hanging requests
- **Graceful failure**: Falls back through multiple proxies before returning error

### Frontend Interface
- **Bootstrap dark theme**: Modern, responsive UI using Bootstrap with dark theme
- **Interactive API testing**: Built-in form for testing API endpoints directly from the browser
- **Real-time status checking**: JavaScript-based health check display
- **Comprehensive documentation**: Dedicated documentation page with examples and usage guides

### Application Structure
- **Modular design**: Separated concerns with dedicated modules for scraping, configuration, and main application
- **Template-based rendering**: Uses Jinja2 templates for HTML generation
- **Static asset serving**: Serves CSS and other static files through Flask
- **Health check endpoint**: Provides system status monitoring capabilities

## External Dependencies

### Core Python Libraries
- **Flask**: Web framework for API endpoints and routing
- **requests**: HTTP library for making web requests with proxy support
- **BeautifulSoup4**: HTML parsing for extracting Open Graph tags
- **flask-cors**: Cross-Origin Resource Sharing support

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive UI components
- **Feather Icons**: Icon library for UI elements
- **Custom CSS**: Additional styling for enhanced user experience

### Proxy Service Integration
- **proxy-seller.com**: Default proxy service provider (configurable)
- **SOCKS5 protocol**: Proxy communication protocol
- **Port range support**: Configurable proxy port ranges (default: 10000-10100)
- **Authentication**: Username/password-based proxy authentication

### Environment Configuration
- **Proxy credentials**: Username, password, IP, and port configuration
- **Request timeout**: Configurable timeout values for web requests
- **Retry limits**: Maximum retry attempts for failed requests
- **Session secrets**: Flask session security configuration

### Development and Deployment
- **Environment variables**: All sensitive configuration through environment variables
- **Debug mode**: Development-friendly error reporting and auto-reload
- **CORS configuration**: Cross-origin request handling for API consumption
- **Health monitoring**: Built-in health check endpoint for monitoring services 