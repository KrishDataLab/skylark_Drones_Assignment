import sys
import os

# Ensure project root is in Python path for Vercel Serverless environment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.main import app
