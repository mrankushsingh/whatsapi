import os
import re
from typing import Dict, List, Any

def get_proxy_config() -> Dict[str, Any]:
    """
    Get proxy configuration from environment variables
    """
    return {
        "ip": os.environ.get("PROXY_IP", "res.proxy-seller.com"),
        "protocol": os.environ.get("PROXY_PROTOCOL", "socks5"),
        "ports": list(range(
            int(os.environ.get("PROXY_PORT_START", "10000")),
            int(os.environ.get("PROXY_PORT_END", "10100"))
        )),
        "username": os.environ.get("PROXY_USERNAME", "817d7b38c9723afb"),
        "password": os.environ.get("PROXY_PASSWORD", "7Ka2o36p"),
    }

def build_proxy_dict(ip: str, port: int, username: str, password: str, protocol: str = "socks5") -> Dict[str, str]:
    """
    Build proxy dictionary for requests
    """
    proxy_url = f"{protocol}://{username}:{password}@{ip}:{port}"
    return {"http": proxy_url, "https": proxy_url}

def get_proxies_list() -> List[Dict[str, str]]:
    """
    Generate list of proxy configurations
    """
    proxy_config = get_proxy_config()
    return [
        build_proxy_dict(
            proxy_config["ip"],
            port,
            proxy_config["username"],
            proxy_config["password"],
            proxy_config["protocol"]
        ) for port in proxy_config["ports"]
    ]

def validate_whatsapp_link(link: str) -> Dict[str, Any]:
    """
    Validate WhatsApp group link format
    
    Args:
        link: The URL to validate
        
    Returns:
        Dict with 'valid' boolean and 'message' string
    """
    if not link:
        return {
            "valid": False,
            "message": "Link cannot be empty"
        }
    
    if not isinstance(link, str):
        return {
            "valid": False,
            "message": "Link must be a string"
        }
    
    # Check if it starts with the correct WhatsApp domain
    if not link.startswith("https://chat.whatsapp.com/"):
        return {
            "valid": False,
            "message": "Link must be a valid WhatsApp group invite link starting with 'https://chat.whatsapp.com/'"
        }
    
    # Extract the group code part
    group_code = link.replace("https://chat.whatsapp.com/", "")
    
    if not group_code:
        return {
            "valid": False,
            "message": "WhatsApp group code is missing from the link"
        }
    
    # Validate group code format - be more permissive
    # WhatsApp group codes can contain various characters
    if len(group_code) < 3 or len(group_code) > 100:
        return {
            "valid": False,
            "message": "WhatsApp group code length should be between 3 and 100 characters."
        }
    
    # Allow most printable characters except spaces and some problematic ones
    if not re.match(r'^[A-Za-z0-9_\-+=/.]+$', group_code):
        return {
            "valid": False,
            "message": "WhatsApp group code contains invalid characters."
        }
    
    return {
        "valid": True,
        "message": "Valid WhatsApp group link"
    }

def get_request_headers() -> Dict[str, str]:
    """
    Get headers for web scraping requests
    """
    return {
        "User-Agent": os.environ.get(
            "USER_AGENT", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
