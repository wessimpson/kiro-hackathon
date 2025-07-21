"""
Knowledge Graph Data Models for AI Job Application Assistant

Defines the node types, relationships, and data structures for the Neo4j knowledge graph.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# Enums for standardized values
class SkillCategory(str, Enum):
    TECHNICAL = "technical"
    SOFT = "soft"
    LANGUAGE = "language"
    CERTIFICATION = "certification"


class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class CompanySize(str, Enum):
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class ImportanceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RequirementType(str, Enum):
    MANDATORY = "mandatory"
    PREFERRED = "preferred"
    NICE_TO_HAVE = "nice_to_have"


# Base Node Classes
class BaseNode(BaseModel):
    """Base class for all knowledge graph nodes"""
    id: str
    type: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# User Repository Knowledge Graph Nodes
class UserNode(BaseNode):
    """User node in the knowledge graph"""
    type: str = "USER"
    user_id: str
    name: str
    email: str
    location: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None


class SkillNode(BaseNode):
    """Skill node representing user capabilities"""
    type: str = "SKILL"
    name: str
    category: SkillCategory
    proficiency: Optional[ProficiencyLevel] = None
    years_of_experience: Optional[int] = None
    last_used: Optional[datetime] = None
    verified: bool = False


class ExperienceNode(BaseNode):
    """Work experience node"""
    type: str = "EXPERIENCE"
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime] = None
    description: str
    achievements: List[str] = []
    location: Optional[str] = None
    is_current: bool = False


class ProjectNode(BaseNode):
    """Project node representing user projects"""
    type: str = "PROJECT"
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None
    github_url: Optional[str] = None
    completion_date: Optional[datetime] = None
    status: str = "completed"  # completed, in_progress, planned


class EducationNode(BaseNode):
    """Education node for academic background"""
    type: str = "EDUCATION"
    institution: str
    degree: str
    field_of_study: str
    start_date: datetime
    end_date: Optional[datetime] = None
    gpa: Optional[float] = None
    honors: List[str] = []


class CertificationNode(BaseNode):
    """Certification node for professional certifications"""
    type: str = "CERTIFICATION"
    name: str
    issuing_organization: str
    issue_date: datetime
    expiration_date: Optional[datetime] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


# Company Repository Knowledge Graph Nodes
class CompanyNode(BaseNode):
    """Company node in the knowledge graph"""
    type: str = "COMPANY"
    name: str
    industry: str
    size: CompanySize
    website: str
    description: str
    headquarters: Optional[str] = None
    founded_year: Optional[int] = None


class JobPostingNode(BaseNode):
    """Job posting node"""
    type: str = "JOB_POSTING"
    title: str
    description: str
    location: str
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    posted_date: datetime
    application_deadline: Optional[datetime] = None
    url: str
    job_type: str = "full_time"  # full_time, part_time, contract, internship
    remote_allowed: bool = False


class RequirementNode(BaseNode):
    """Job requirement node"""
    type: str = "REQUIREMENT"
    skill: str
    importance: ImportanceLevel
    years_required: Optional[int] = None
    requirement_type: RequirementType
    description: Optional[str] = None


class CompanyNewsNode(BaseNode):
    """Company news and events node"""
    type: str = "COMPANY_NEWS"
    title: str
    content: str
    published_date: datetime
    source: str
    url: Optional[str] = None
    sentiment: Optional[str] = None  # positive, negative, neutral


# Relationship Models
class BaseRelationship(BaseModel):
    """Base class for all relationships"""
    type: str
    created_at: datetime = Field(default_factory=datetime.now)
    properties: Dict[str, Any] = {}


class UserSkillRelationship(BaseRelationship):
    """Relationship between user and skill"""
    type: str = "HAS_SKILL"
    proficiency: ProficiencyLevel
    years_of_experience: int
    last_used: datetime
    verified: bool = False


class ExperienceSkillRelationship(BaseRelationship):
    """Relationship between experience and skill"""
    type: str = "USED_SKILL"
    frequency: str  # daily, weekly, monthly, occasionally
    impact: str  # high, medium, low


class ProjectSkillRelationship(BaseRelationship):
    """Relationship between project and skill"""
    type: str = "DEMONSTRATES_SKILL"
    complexity: str  # basic, intermediate, advanced
    role: str  # primary, secondary, supporting


class CompanyJobRelationship(BaseRelationship):
    """Relationship between company and job posting"""
    type: str = "OFFERS_JOB"
    department: Optional[str] = None
    urgency: str = "normal"  # urgent, normal, low


class JobRequirementRelationship(BaseRelationship):
    """Relationship between job and requirement"""
    type: str = "REQUIRES_SKILL"
    importance: ImportanceLevel
    years_required: Optional[int] = None
    mandatory: bool = True


class UserJobMatchRelationship(BaseRelationship):
    """Relationship representing job match for user"""
    type: str = "MATCHES_JOB"
    compatibility_score: float
    skill_match_percentage: float
    experience_match: float
    calculated_at: datetime = Field(default_factory=datetime.now)


# Composite Models for API Responses
class UserRepository(BaseModel):
    """Complete user repository model"""
    user: UserNode
    skills: List[SkillNode] = []
    experiences: List[ExperienceNode] = []
    projects: List[ProjectNode] = []
    education: List[EducationNode] = []
    certifications: List[CertificationNode] = []


class CompanyRepository(BaseModel):
    """Complete company repository model"""
    company: CompanyNode
    job_postings: List[JobPostingNode] = []
    news: List[CompanyNewsNode] = []


class JobMatch(BaseModel):
    """Job matching result model"""
    job: JobPostingNode
    company: CompanyNode
    compatibility_score: float
    skill_matches: List[Dict[str, Any]] = []
    missing_skills: List[str] = []
    recommendations: List[str] = []


# Vector Database Models
class VectorDocument(BaseModel):
    """Model for vector database documents"""
    id: str
    vector: List[float]
    metadata: Dict[str, Any]
    content: str
    document_type: str  # resume, job_description, company_info, project
    timestamp: datetime = Field(default_factory=datetime.now)


# Configuration Models
class KnowledgeGraphConfig(BaseModel):
    """Configuration for knowledge graph operations"""
    neo4j_uri: str
    neo4j_user: str
    neo4j_password: str
    database: str = "neo4j"
    max_connection_pool_size: int = 50
    connection_timeout: int = 30


class VectorDBConfig(BaseModel):
    """Configuration for vector database operations"""
    pinecone_api_key: str
    pinecone_environment: str
    index_name: str
    dimension: int = 1536  # OpenAI embedding dimension
    metric: str = "cosine"