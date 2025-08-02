import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scraper import scrape_og_tags
from config import validate_whatsapp_link

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Enable CORS for all routes
CORS(app)

@app.route('/')
def index():
    """Home page with API documentation"""
    return render_template('index.html')

@app.route('/docs')
def docs():
    """API documentation page"""
    return render_template('docs.html')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "WhatsApp Group Link Scraper API is running",
        "version": "1.0.0"
    }), 200

@app.route('/test-scrape', methods=['POST'])
def test_scrape():
    """
    Test scraping endpoint for HTML form submission
    """
    try:
        link = request.form.get('link')
        if not link:
            return render_template('index.html', error="Missing WhatsApp group link")
        
        # Validate WhatsApp link format
        validation_result = validate_whatsapp_link(link)
        if not validation_result["valid"]:
            return render_template('index.html', error=validation_result["message"])
        
        # Log the scraping attempt
        logger.info(f"Attempting to scrape: {link}")
        
        # Perform scraping
        result = scrape_og_tags(link)
        
        # Add the original link to the response
        if "error" not in result:
            result["link"] = link
            logger.info(f"Successfully scraped: {link}")
            return render_template('index.html', success=True, result=result)
        else:
            logger.error(f"Failed to scrape: {link} - {result['error']}")
            return render_template('index.html', error=result['error'])
    
    except Exception as e:
        logger.error(f"Unexpected error in /test-scrape endpoint: {str(e)}")
        return render_template('index.html', error="Internal server error occurred while processing the request")

@app.route('/scrape', methods=['POST'])
def scrape():
    """
    Scrape WhatsApp group link metadata
    
    Expected JSON payload:
    {
        "link": "https://chat.whatsapp.com/XXXXXXXXX"
    }
    
    Returns:
    {
        "og_title": "Group Name",
        "og_image": "https://...",
        "link": "https://chat.whatsapp.com/XXXXXXXXX"
    }
    """
    try:
        # Validate content type
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400
        
        link = data.get('link')
        if not link:
            return jsonify({
                "error": "Missing required field: 'link'"
            }), 400
        
        # Validate WhatsApp link format
        validation_result = validate_whatsapp_link(link)
        if not validation_result["valid"]:
            return jsonify({
                "error": validation_result["message"]
            }), 400
        
        # Log the scraping attempt
        logger.info(f"Attempting to scrape: {link}")
        
        # Perform scraping
        result = scrape_og_tags(link)
        
        # Add the original link to the response
        if "error" not in result:
            result["link"] = link
            logger.info(f"Successfully scraped: {link}")
        else:
            logger.error(f"Failed to scrape: {link} - {result['error']}")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Unexpected error in /scrape endpoint: {str(e)}")
        return jsonify({
            "error": "Internal server error occurred while processing the request"
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist. Check /docs for available endpoints."
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "error": "Method not allowed",
        "message": "The HTTP method is not allowed for this endpoint. Check /docs for available methods."
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred. Please try again later."
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
