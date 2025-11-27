"""
Vercel serverless function entry point for FastAPI application
"""
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import app modules
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Change to parent directory for relative imports
os.chdir(parent_dir)

from main import app
from mangum import Mangum

# Wrap FastAPI app with Mangum for AWS Lambda/Vercel compatibility
handler = Mangum(app, lifespan="off")

