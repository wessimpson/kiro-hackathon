"""
PostgreSQL Database Models for Authentication and Application Tracking
"""
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
import enum

Base = declarative_base()


class ApplicationStatus(enum.Enum):
    """Application status enumeration"""
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    WITHDRAWN = "WITHDRAWN"


class User(Base):
    """User authentication and profile table"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    applications = relationship("Application", back_populates="user")
    user_preferences = relationship("UserPreferences", back_populates="user", uselist=False)


class UserPreferences(Base):
    """User job search preferences"""
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Job search preferences
    preferred_locations = Column(Text, nullable=True)  # JSON array of locations
    preferred_job_types = Column(Text, nullable=True)  # JSON array of job types
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    remote_work_preference = Column(String(50), default="FLEXIBLE")  # REMOTE_ONLY, HYBRID, ON_SITE, FLEXIBLE
    
    # Automation settings
    auto_apply_enabled = Column(Boolean, default=False)
    min_match_score = Column(Integer, default=70)  # Minimum match score for auto-apply
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="user_preferences")


class Application(Base):
    """Job application tracking table"""
    __tablename__ = "applications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Job information
    job_posting_id = Column(String(255), nullable=False)  # Reference to Neo4j job node
    company_name = Column(String(255), nullable=False)
    job_title = Column(String(255), nullable=False)
    job_url = Column(Text, nullable=True)
    
    # Application details
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    ats_score = Column(Integer, nullable=True)
    match_score = Column(Integer, nullable=True)
    
    # Generated documents
    resume_version = Column(Text, nullable=True)  # JSON of resume data
    cover_letter_content = Column(Text, nullable=True)
    
    # Tracking information
    submitted_at = Column(DateTime, nullable=True)
    response_received_at = Column(DateTime, nullable=True)
    interview_scheduled_at = Column(DateTime, nullable=True)
    final_decision_at = Column(DateTime, nullable=True)
    
    # Notes and feedback
    notes = Column(Text, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    application_events = relationship("ApplicationEvent", back_populates="application")


class ApplicationEvent(Base):
    """Application event tracking for analytics"""
    __tablename__ = "application_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    
    event_type = Column(String(100), nullable=False)  # CREATED, SUBMITTED, VIEWED, RESPONDED, etc.
    event_data = Column(Text, nullable=True)  # JSON data for event details
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    application = relationship("Application", back_populates="application_events")


class SystemConfig(Base):
    """System configuration and metadata"""
    __tablename__ = "system_config"
    
    key = Column(String(255), primary_key=True)
    value = Column(Text, nullable=False)  # JSON value
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class JobSearchSession(Base):
    """Job search session tracking for analytics"""
    __tablename__ = "job_search_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    jobs_viewed = Column(Integer, default=0)
    applications_created = Column(Integer, default=0)
    applications_submitted = Column(Integer, default=0)
    
    # Session metadata
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Relationships
    user = relationship("User")


class UserAnalytics(Base):
    """User analytics and performance metrics"""
    __tablename__ = "user_analytics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Performance metrics
    total_applications = Column(Integer, default=0)
    total_responses = Column(Integer, default=0)
    total_interviews = Column(Integer, default=0)
    total_offers = Column(Integer, default=0)
    
    # Success rates
    response_rate = Column(Integer, default=0)  # Percentage
    interview_rate = Column(Integer, default=0)  # Percentage
    offer_rate = Column(Integer, default=0)  # Percentage
    
    # Average scores
    avg_ats_score = Column(Integer, default=0)
    avg_match_score = Column(Integer, default=0)
    
    # Time metrics
    avg_response_time_days = Column(Integer, default=0)
    
    last_calculated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

# Data
#base initialization and utility functions
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Database engine and session
engine = create_engine(settings.postgresql_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("PostgreSQL database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize PostgreSQL database: {e}")
        raise


def create_default_config():
    """Create default system configuration"""
    db = SessionLocal()
    try:
        # Check if config already exists
        existing_config = db.query(SystemConfig).first()
        if not existing_config:
            default_configs = [
                SystemConfig(
                    key="app_version",
                    value="1.0.0",
                    description="Application version"
                ),
                SystemConfig(
                    key="maintenance_mode",
                    value="false",
                    description="Maintenance mode flag"
                ),
                SystemConfig(
                    key="max_applications_per_day",
                    value="50",
                    description="Maximum applications per user per day"
                )
            ]
            
            for config in default_configs:
                db.add(config)
            
            db.commit()
            logger.info("Default system configuration created")
    except Exception as e:
        logger.error(f"Failed to create default configuration: {e}")
        db.rollback()
    finally:
        db.close()