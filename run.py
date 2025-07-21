#!/usr/bin/env python3
"""
AI Job Application Assistant - Development Server

Run this script to start the development server with all dependencies.
"""
import uvicorn
import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.config.settings import settings


def main():
    """Start the development server"""
    print("🚀 Starting AI Job Application Assistant...")
    print(f"📊 Debug mode: {settings.debug}")
    print(f"🔗 Neo4j URI: {settings.neo4j_uri}")
    print(f"🐘 PostgreSQL URL: {settings.postgresql_url}")
    print("=" * 50)
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )


if __name__ == "__main__":
    main()