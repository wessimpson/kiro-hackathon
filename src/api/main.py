"""
FastAPI Main Application
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from src.config.settings import settings
from src.database.neo4j_client import neo4j_client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AI Job Application Assistant")
    try:
        # Initialize Neo4j connection
        neo4j_client.connect()
        neo4j_client.setup_indexes()
        logger.info("Database connections established")
    except Exception as e:
        logger.error(f"Failed to initialize databases: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Job Application Assistant")
    neo4j_client.close()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="AI-powered job application assistant using CrewAI agents and knowledge graphs",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Job Application Assistant API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test Neo4j connection
        neo4j_client.execute_query("RETURN 1")
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )