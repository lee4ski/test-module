"""
Vercel serverless function entry point for FastAPI application
"""
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from main import app
    from mangum import Mangum
    
    # Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # For debugging - this will show in Vercel logs
    def handler(event, context):
        return {
            "statusCode": 500,
            "body": f"Error initializing app: {str(e)}"
        }

