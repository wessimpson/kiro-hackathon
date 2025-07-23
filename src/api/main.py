"""
FastAPI Main Application
"""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from src.config.settings import settings
from src.database.neo4j_client import neo4j_client
from src.services.job_monitoring_service import job_monitoring_service

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
        
        # Start job monitoring service
        await job_monitoring_service.start_monitoring()
        logger.info("Job monitoring service started")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Job Application Assistant")
    await job_monitoring_service.stop_monitoring()
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

# Include API routes
from .routes.notifications import router as notifications_router
from .routes.jobs import router as jobs_router

app.include_router(notifications_router, prefix="/api/v1/notifications", tags=["notifications"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])


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