import os
import requests
from bs4 import BeautifulSoup, Tag
import random
import logging
from typing import Dict, Any
from config import get_proxies_list, get_request_headers

logger = logging.getLogger(__name__)

def scrape_og_tags(link: str) -> Dict[str, Any]:
    """
    Scrape Open Graph tags from WhatsApp group link
    
    Args:
        link: WhatsApp group invite link
        
    Returns:
        Dictionary containing og_title, og_image, or error message
    """
    proxies_list = get_proxies_list()
    headers = get_request_headers()
    
    # Timeout configuration
    timeout = int(os.environ.get("REQUEST_TIMEOUT", "10"))
    max_retries = int(os.environ.get("MAX_RETRIES", "3"))
    
    # Try scraping with different proxies
    attempts = min(len(proxies_list), max_retries)
    
    for attempt in range(attempts):
        proxy = random.choice(proxies_list)
        
        try:
            logger.debug(f"Attempt {attempt + 1}/{attempts} - Using proxy: {proxy['https'].split('@')[1]}")
            
            # Make request with proxy
            response = requests.get(
                link,
                headers=headers,
                proxies=proxy,
                timeout=timeout,
                allow_redirects=True
            )
            
            # Check if request was successful
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract Open Graph tags
            og_title = soup.find('meta', property='og:title')
            og_image = soup.find('meta', property='og:image')
            og_description = soup.find('meta', property='og:description')
            og_url = soup.find('meta', property='og:url')
            
            # Extract content from meta tags
            title = og_title.get('content') if isinstance(og_title, Tag) else None
            image = og_image.get('content') if isinstance(og_image, Tag) else None
            description = og_description.get('content') if isinstance(og_description, Tag) else None
            url = og_url.get('content') if isinstance(og_url, Tag) else None
            
            # Also try to get title from <title> tag if og:title is not available
            if not title:
                title_tag = soup.find('title')
                title = title_tag.get_text().strip() if title_tag else None
            
            # Log successful extraction
            logger.info(f"Successfully extracted metadata from {link}")
            logger.debug(f"Title: {title}, Image: {image}")
            
            result = {
                "og_title": title,
                "og_image": image
            }
            
            # Add optional fields if available
            if description:
                result["og_description"] = description
            if url:
                result["og_url"] = url
            
            return result
            
        except requests.exceptions.ProxyError as e:
            logger.warning(f"Proxy error on attempt {attempt + 1}: {str(e)}")
            continue
            
        except requests.exceptions.Timeout as e:
            logger.warning(f"Timeout error on attempt {attempt + 1}: {str(e)}")
            continue
            
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error on attempt {attempt + 1}: {str(e)}")
            continue
            
        except requests.exceptions.HTTPError as e:
            logger.warning(f"HTTP error on attempt {attempt + 1}: {str(e)}")
            # If it's a 4xx error, don't retry as it's likely not a proxy issue
            if hasattr(e, 'response') and e.response and 400 <= e.response.status_code < 500:
                return {
                    "error": f"HTTP {e.response.status_code}: Unable to access the WhatsApp group link. The link may be invalid or expired."
                }
            continue
            
        except Exception as e:
            logger.warning(f"Unexpected error on attempt {attempt + 1}: {str(e)}")
            continue
    
    # All attempts failed
    logger.error(f"All {attempts} proxy attempts failed for {link}")
    return {
        "error": f"Unable to scrape the link after {attempts} attempts. All proxies failed or the link may be inaccessible."
    }


