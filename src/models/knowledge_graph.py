"""
Knowledge Graph Data Models for AI Job Application Assistant

Defines the node types, relationships, and data structures for the Neo4j knowledge graph.
All models use strict Pydantic validation for type safety and data integrity.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import re


# Base configuration for all Pydantic models
class BaseConfig:
    use_enum_values = True
    validate_assignment = True
    arbitrary_types_allowed = True


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


class SocialPlatform(str, Enum):
    LINKEDIN = "linkedin"
    GITHUB = "github"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"


class DocumentType(str, Enum):
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    RECOMMENDATION = "recommendation"
    PORTFOLIO = "portfolio"


class JobStatus(str, Enum):
    INTERESTED = "interested"
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    REJECTED = "rejected"
    OFFER = "offer"
    WITHDRAWN = "withdrawn"


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
    user_id: str = Field(..., description="User's unique identifier")
    name: str = Field(..., min_length=1, description="User's full name")
    email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$', description="User's email address")
    location: Optional[str] = Field(None, description="User's location")
    phone: Optional[str] = Field(None, description="User's phone number")
    linkedin_url: Optional[str] = Field(None, regex=r'^https?://(www\.)?linkedin\.com/', description="LinkedIn profile URL")
    github_url: Optional[str] = Field(None, regex=r'^https?://(www\.)?github\.com/', description="GitHub profile URL")
    portfolio_url: Optional[str] = Field(None, regex=r'^https?://', description="Portfolio website URL")
    
    class Config(BaseConfig):
        pass


class SkillNode(BaseNode):
    """Skill node representing user capabilities"""
    type: str = "SKILL"
    name: str = Field(..., min_length=1, description="Skill name")
    category: SkillCategory = Field(..., description="Skill category")
    proficiency: Optional[ProficiencyLevel] = Field(None, description="Proficiency level")
    years_of_experience: Optional[int] = Field(None, ge=0, le=50, description="Years of experience with this skill")
    last_used: Optional[datetime] = Field(None, description="Last time skill was used")
    verified: bool = Field(default=False, description="Whether skill is verified by experience/project evidence")
    
    @validator('years_of_experience')
    def validate_experience(cls, v):
        if v is not None and v > 50:
            raise ValueError('Years of experience cannot exceed 50')
        return v
    
    class Config(BaseConfig):
        pass


class ExperienceNode(BaseNode):
    """Work experience node"""
    type: str = "EXPERIENCE"
    company: str = Field(..., min_length=1, description="Company name")
    position: str = Field(..., min_length=1, description="Job position/title")
    start_date: datetime = Field(..., description="Start date of employment")
    end_date: Optional[datetime] = Field(None, description="End date of employment")
    description: str = Field(..., min_length=10, description="Job description")
    achievements: List[str] = Field(default_factory=list, description="List of achievements")
    location: Optional[str] = Field(None, description="Job location")
    is_current: bool = Field(default=False, description="Whether this is current employment")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date cannot be before start date')
        return v
    
    class Config(BaseConfig):
        pass


class ProjectNode(BaseNode):
    """Project node representing user projects"""
    type: str = "PROJECT"
    name: str = Field(..., min_length=1, description="Project name")
    description: str = Field(..., min_length=10, description="Project description")
    technologies: List[str] = Field(..., min_items=1, description="Technologies used in the project")
    url: Optional[str] = Field(None, regex=r'^https?://', description="Project URL")
    github_url: Optional[str] = Field(None, regex=r'^https?://(www\.)?github\.com/', description="GitHub repository URL")
    completion_date: Optional[datetime] = Field(None, description="Project completion date")
    status: str = Field(default="completed", description="Project status")  # completed, in_progress, planned
    
    class Config(BaseConfig):
        pass


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

#Agent Communication Models for CrewAI

class ProfileData(BaseModel):
    """Social media profile data extracted by User Repository Agent"""
    platform: SocialPlatform = Field(..., description="Social media platform")
    url: str = Field(..., regex=r'^https?://', description="Profile URL")
    extracted_data: Dict[str, Any] = Field(..., description="Extracted profile data")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence score")
    extraction_timestamp: datetime = Field(default_factory=datetime.now, description="When data was extracted")
    
    class Config(BaseConfig):
        pass


class ExtractedData(BaseModel):
    """Data extracted from documents or profiles"""
    content: str = Field(..., min_length=1, description="Extracted content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    extraction_method: str = Field(..., description="Method used for extraction")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in extraction accuracy")
    
    class Config(BaseConfig):
        pass


class Recommendation(BaseModel):
    """Improvement recommendation from agents"""
    id: str = Field(..., description="Unique recommendation ID")
    type: str = Field(..., description="Type of recommendation")
    title: str = Field(..., min_length=1, description="Recommendation title")
    description: str = Field(..., min_length=10, description="Detailed description")
    priority: ImportanceLevel = Field(..., description="Priority level")
    estimated_impact: float = Field(..., ge=0.0, le=1.0, description="Expected impact score")
    implementation_effort: str = Field(..., description="Effort required to implement")
    
    class Config(BaseConfig):
        pass


class ManualJobInput(BaseModel):
    """Manual job input from user for Job Input Management Agent"""
    title: str = Field(..., min_length=1, description="Job title")
    company_name: str = Field(..., min_length=1, description="Company name")
    company_website: Optional[str] = Field(None, regex=r'^https?://', description="Company website URL")
    job_description: str = Field(..., min_length=50, description="Full job description")
    location: str = Field(..., min_length=1, description="Job location")
    salary_min: Optional[int] = Field(None, ge=0, description="Minimum salary")
    salary_max: Optional[int] = Field(None, ge=0, description="Maximum salary")
    application_url: Optional[str] = Field(None, regex=r'^https?://', description="Application URL")
    job_type: str = Field(default="full_time", description="Job type")
    remote_allowed: bool = Field(default=False, description="Remote work allowed")
    user_notes: Optional[str] = Field(None, description="User's personal notes")
    status: JobStatus = Field(default=JobStatus.INTERESTED, description="Application status")
    
    @validator('salary_max')
    def validate_salary_range(cls, v, values):
        if v and 'salary_min' in values and values['salary_min'] and v < values['salary_min']:
            raise ValueError('Maximum salary cannot be less than minimum salary')
        return v
    
    class Config(BaseConfig):
        pass


class ProcessedJobPosting(BaseModel):
    """Processed job posting from Job Input Management Agent"""
    id: str = Field(..., description="Generated job posting ID")
    original_input: ManualJobInput = Field(..., description="Original user input")
    extracted_requirements: List[str] = Field(default_factory=list, description="Extracted job requirements")
    skill_keywords: List[str] = Field(default_factory=list, description="Identified skill keywords")
    experience_level: str = Field(..., description="Required experience level")
    company_id: Optional[str] = Field(None, description="Associated company ID if found")
    processing_timestamp: datetime = Field(default_factory=datetime.now, description="Processing timestamp")
    
    class Config(BaseConfig):
        pass


class CompanyData(BaseModel):
    """Company data extracted by Company Repository Agent"""
    name: str = Field(..., min_length=1, description="Company name")
    website: str = Field(..., regex=r'^https?://', description="Company website URL")
    industry: str = Field(..., min_length=1, description="Company industry")
    size: CompanySize = Field(..., description="Company size category")
    description: str = Field(..., min_length=10, description="Company description")
    culture_keywords: List[str] = Field(default_factory=list, description="Company culture keywords")
    technologies: List[str] = Field(default_factory=list, description="Technologies used by company")
    scraped_at: datetime = Field(default_factory=datetime.now, description="When data was scraped")
    
    class Config(BaseConfig):
        pass


class NewsData(BaseModel):
    """Company news data for Cover Letter Agent"""
    title: str = Field(..., min_length=1, description="News article title")
    content: str = Field(..., min_length=10, description="News content")
    source: str = Field(..., min_length=1, description="News source")
    published_date: datetime = Field(..., description="Publication date")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance to company")
    sentiment: str = Field(..., regex=r'^(positive|negative|neutral)$', description="Article sentiment")
    
    class Config(BaseConfig):
        pass


class SalaryRange(BaseModel):
    """Salary range information"""
    min_salary: Optional[int] = Field(None, ge=0, description="Minimum salary")
    max_salary: Optional[int] = Field(None, ge=0, description="Maximum salary")
    currency: str = Field(default="USD", description="Currency code")
    
    @validator('max_salary')
    def validate_salary_range(cls, v, values):
        if v and 'min_salary' in values and values['min_salary'] and v < values['min_salary']:
            raise ValueError('Maximum salary cannot be less than minimum salary')
        return v
    
    class Config(BaseConfig):
        pass


class Resume(BaseModel):
    """Resume generated by Resume Generation Agent"""
    id: str = Field(..., description="Resume ID")
    user_id: str = Field(..., description="User ID")
    job_id: str = Field(..., description="Target job ID")
    content: Dict[str, Any] = Field(..., description="Resume content structure")
    format_type: str = Field(default="ats_optimized", description="Resume format type")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    ats_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="ATS compatibility score")
    
    class Config(BaseConfig):
        pass


class CoverLetter(BaseModel):
    """Cover letter generated by Cover Letter Agent"""
    id: str = Field(..., description="Cover letter ID")
    user_id: str = Field(..., description="User ID")
    job_id: str = Field(..., description="Target job ID")
    company_id: str = Field(..., description="Target company ID")
    content: str = Field(..., min_length=100, description="Cover letter content")
    tone: str = Field(default="professional", description="Cover letter tone")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation timestamp")
    company_insights_used: List[str] = Field(default_factory=list, description="Company insights incorporated")
    
    class Config(BaseConfig):
        pass


class ATSScore(BaseModel):
    """ATS compatibility score from ATS Scoring Agent"""
    score: float = Field(..., ge=0.0, le=100.0, description="Overall ATS score")
    keyword_match: float = Field(..., ge=0.0, le=100.0, description="Keyword matching score")
    format_score: float = Field(..., ge=0.0, le=100.0, description="Format compatibility score")
    structure_score: float = Field(..., ge=0.0, le=100.0, description="Structure score")
    recommendations: List[Recommendation] = Field(default_factory=list, description="Improvement recommendations")
    calculated_at: datetime = Field(default_factory=datetime.now, description="Calculation timestamp")
    
    class Config(BaseConfig):
        pass


class SkillGap(BaseModel):
    """Skill gap identified by Project Recommendation Agent"""
    skill_name: str = Field(..., min_length=1, description="Missing skill name")
    importance: ImportanceLevel = Field(..., description="Importance for target job")
    current_level: Optional[ProficiencyLevel] = Field(None, description="Current proficiency level")
    required_level: ProficiencyLevel = Field(..., description="Required proficiency level")
    gap_severity: float = Field(..., ge=0.0, le=1.0, description="Gap severity score")
    
    class Config(BaseConfig):
        pass


class ProjectRecommendation(BaseModel):
    """Project recommendation from Project Recommendation Agent"""
    id: str = Field(..., description="Recommendation ID")
    title: str = Field(..., min_length=1, description="Project title")
    description: str = Field(..., min_length=50, description="Project description")
    skills_addressed: List[str] = Field(..., min_items=1, description="Skills this project addresses")
    difficulty_level: str = Field(..., description="Project difficulty level")
    estimated_duration: str = Field(..., description="Estimated completion time")
    technologies: List[str] = Field(..., min_items=1, description="Technologies to be used")
    deliverables: List[str] = Field(..., min_items=1, description="Expected deliverables")
    impact_score: float = Field(..., ge=0.0, le=1.0, description="Expected impact on job prospects")
    
    class Config(BaseConfig):
        pass


class ImplementationPlan(BaseModel):
    """Implementation plan for recommended projects"""
    project_id: str = Field(..., description="Associated project recommendation ID")
    phases: List[Dict[str, Any]] = Field(..., min_items=1, description="Project phases")
    milestones: List[Dict[str, Any]] = Field(..., description="Project milestones")
    resources_needed: List[str] = Field(default_factory=list, description="Required resources")
    success_criteria: List[str] = Field(..., min_items=1, description="Success criteria")
    timeline: Dict[str, Any] = Field(..., description="Detailed timeline")
    
    class Config(BaseConfig):
        pass


class ValidationResult(BaseModel):
    """Validation result for job input"""
    is_valid: bool = Field(..., description="Whether input is valid")
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    
    class Config(BaseConfig):
        pass


# Enhanced composite models with strict validation
class UserRepositoryComplete(BaseModel):
    """Complete user repository with all data and validation"""
    id: str = Field(..., description="Repository ID")
    user_id: str = Field(..., description="User ID")
    personal_info: Dict[str, Any] = Field(..., description="Personal information")
    experiences: List[ExperienceNode] = Field(default_factory=list, description="Work experiences")
    skills: List[SkillNode] = Field(default_factory=list, description="Skills with verification status")
    projects: List[ProjectNode] = Field(default_factory=list, description="Projects")
    social_profiles: List[ProfileData] = Field(default_factory=list, description="Social media profiles")
    documents: List[Dict[str, Any]] = Field(default_factory=list, description="Uploaded documents")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    @validator('skills')
    def validate_skill_verification(cls, v):
        """Ensure all skills have proper verification status"""
        for skill in v:
            if skill.verified and not any([skill.years_of_experience, skill.last_used]):
                raise ValueError(f"Verified skill '{skill.name}' must have experience data")
        return v
    
    class Config(BaseConfig):
        pass


class CompanyRepositoryComplete(BaseModel):
    """Complete company repository with all data and validation"""
    id: str = Field(..., description="Repository ID")
    company_name: str = Field(..., min_length=1, description="Company name")
    website_data: CompanyData = Field(..., description="Scraped website data")
    current_events: List[NewsData] = Field(default_factory=list, description="Recent news and events")
    job_postings: List[JobPostingNode] = Field(default_factory=list, description="Job postings")
    industry_info: Dict[str, Any] = Field(default_factory=dict, description="Industry information")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    
    class Config(BaseConfig):
        pass