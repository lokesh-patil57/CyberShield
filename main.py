import logging
from app import app

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Flask application on port 5000...")
    # Always serve on port 5000 with host 0.0.0.0 to make it accessible
    app.run(host='0.0.0.0', port=5000, debug=True)