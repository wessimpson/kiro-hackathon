# AI Job Application Assistant - Comprehensive Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Package Dependencies](#package-dependencies)
4. [File Structure & Components](#file-structure--components)
5. [Data Flow Diagrams](#data-flow-diagrams)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Agent System](#agent-system)
9. [Service Layer](#service-layer)
10. [Setup & Deployment](#setup--deployment)

## System Overview

The AI Job Application Assistant is an intelligent platform that automates and optimizes job applications using CrewAI agents and knowledge graphs. The system transforms job searching from manual work into an intelligent, automated process.

### Core Features
- **User Repository Creation**: Analyzes social profiles and documents to build professional profiles
- **Company Intelligence**: Scrapes company websites and monitors events
- **AI-Generated Applications**: Creates tailored resumes and cover letters
- **ATS Optimization**: Scores and optimizes applications for tracking systems
- **Autonomous Job Discovery**: Monitors job boards and auto-generates applications

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Job Application Assistant                  │
├─────────────────────────────────────────────────────────────────┤
│  Frontend (Web App)                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Dashboard   │  │ Applications│  │ Profile     │            │
│  │             │  │ Manager     │  │ Builder     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  API Layer (FastAPI)                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Jobs API    │  │ Users API   │  │ Notifications│            │
│  │             │  │             │  │ API         │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  Service Layer                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Knowledge   │  │ Application │  │ Job         │            │
│  │ Graph       │  │ Workflow    │  │ Monitoring  │            │
│  │ Service     │  │ Service     │  │ Service     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  Agent Layer (CrewAI)                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ User Repo   │  │ Job         │  │ Resume      │            │
│  │ Agent       │  │ Discovery   │  │ Generation  │            │
│  │             │  │ Agent       │  │ Agent       │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
├─────────────────────────────────────────────────────────────────┤
│  Data Layer                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Neo4j       │  │ PostgreSQL  │  │ Pinecone    │            │
│  │ (Knowledge  │  │ (User Data  │  │ (Vector     │            │
│  │ Graph)      │  │ & Apps)     │  │ Search)     │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## Package Dependencies

### AI & Machine Learning
- **crewai==0.28.8**: Multi-agent AI framework for orchestrating intelligent agents
- **crewai-tools==0.1.6**: Additional tools and utilities for CrewAI agents
- **langchain==0.1.20**: Framework for developing LLM-powered applications
- **langchain-openai==0.1.8**: OpenAI integration for LangChain
- **openai==1.30.5**: OpenAI API client for GPT models

### Web Framework
- **fastapi==0.111.0**: Modern, fast web framework for building APIs
- **uvicorn[standard]==0.30.1**: ASGI server for running FastAPI applications
- **pydantic==2.7.4**: Data validation using Python type annotations
- **pydantic-settings==2.3.4**: Settings management using Pydantic

### Database & Storage
- **neo4j==5.20.0**: Graph database driver for knowledge graph operations
- **psycopg2-binary==2.9.9**: PostgreSQL adapter for Python
- **sqlalchemy==2.0.30**: SQL toolkit and ORM
- **alembic==1.13.1**: Database migration tool for SQLAlchemy
- **pinecone-client==3.2.2**: Vector database for semantic search

### Data Processing
- **pandas==2.2.2**: Data manipulation and analysis library
- **numpy==1.26.4**: Numerical computing library
- **python-multipart==0.0.9**: Multipart form data parsing

### Web Scraping & Automation
- **beautifulsoup4==4.12.3**: HTML/XML parsing library
- **requests==2.32.3**: HTTP library for API calls
- **selenium==4.21.0**: Web browser automation
- **scrapy==2.11.2**: Web scraping framework

### Document Processing
- **python-docx==1.1.0**: Microsoft Word document processing
- **PyPDF2==3.0.1**: PDF file processing
- **python-magic==0.4.27**: File type detection

### Security & Authentication
- **python-jose[cryptography]==3.3.0**: JWT token handling
- **passlib[bcrypt]==1.7.4**: Password hashing library

## File Structure & Components

### Core Application (`src/`)

#### API Layer (`src/api/`)
```
src/api/
├── __init__.py
├── main.py                 # FastAPI application setup and configuration
└── routes/
    ├── jobs.py            # Job monitoring and preferences endpoints
    └── notifications.py   # Notification management endpoints
```

**main.py** - FastAPI Application Entry Point
- **Classes/Functions**:
  - `lifespan()`: Async context manager for app startup/shutdown
  - `app`: FastAPI application instance with CORS middleware
  - `root()`: Root endpoint returning API info
  - `health_check()`: Health monitoring endpoint
- **Dependencies**: FastAPI, Neo4j client, job monitoring service
- **Purpose**: Configures the web server, initializes database connections, starts background services

**routes/jobs.py** - Job Management API
- **Classes**:
  - `JobPreferences`: Pydantic model for user job search preferences
  - `MonitoringStatusResponse`: Response model for monitoring status
- **Endpoints**:
  - `POST /monitoring/enable`: Enable job monitoring for user
  - `POST /monitoring/disable`: Disable job monitoring
  - `GET /monitoring/status`: Get current monitoring status
  - `PUT /monitoring/preferences`: Update job search preferences
  - `GET /monitoring/stats`: Get system monitoring statistics

#### Configuration (`src/config/`)
```
src/config/
├── __init__.py
└── settings.py            # Application settings and environment variables
```

#### Database Layer (`src/database/`)
```
src/database/
├── __init__.py
├── neo4j_client.py        # Neo4j knowledge graph database client
└── postgresql_models.py   # SQLAlchemy models for PostgreSQL
```

**neo4j_client.py** - Knowledge Graph Database Client
- **Classes**:
  - `Neo4jClient`: Main database client class
- **Methods**:
  - `connect()`: Establish Neo4j connection
  - `execute_query()`: Execute Cypher queries
  - `create_node()`: Create knowledge graph nodes
  - `create_relationship()`: Create node relationships
  - `get_user_knowledge_graph()`: Retrieve complete user graph
  - `calculate_job_match_score()`: Calculate user-job compatibility
  - `setup_indexes()`: Create database performance indexes
- **Purpose**: Manages all Neo4j operations for the knowledge graph

**postgresql_models.py** - Relational Database Models
- **Classes**:
  - `User`: User authentication and profile data
  - `UserPreferences`: Job search preferences and settings
  - `Application`: Job application tracking
  - `ApplicationEvent`: Application event logging
  - `SystemConfig`: System configuration storage
  - `JobSearchSession`: User session analytics
  - `UserAnalytics`: Performance metrics and statistics
- **Enums**:
  - `ApplicationStatus`: Application lifecycle states
- **Functions**:
  - `get_db()`: Database session dependency
  - `init_db()`: Initialize database tables
  - `create_default_config()`: Setup default system configuration

#### Models (`src/models/`)
```
src/models/
├── __init__.py
└── knowledge_graph.py     # Pydantic models for knowledge graph entities
```

**knowledge_graph.py** - Knowledge Graph Data Models
- **Base Classes**:
  - `BaseNode`: Base class for all graph nodes
  - `BaseRelationship`: Base class for all relationships
- **Node Types**:
  - `UserNode`: User profile information
  - `SkillNode`: Technical and soft skills
  - `ExperienceNode`: Work experience records
  - `ProjectNode`: User projects and portfolios
  - `EducationNode`: Academic background
  - `CertificationNode`: Professional certifications
  - `CompanyNode`: Company information
  - `JobPostingNode`: Job opportunity details
  - `RequirementNode`: Job requirements
  - `CompanyNewsNode`: Company news and events
- **Relationship Types**:
  - `UserSkillRelationship`: User skill proficiency
  - `ExperienceSkillRelationship`: Skills used in experience
  - `ProjectSkillRelationship`: Skills demonstrated in projects
  - `JobRequirementRelationship`: Job skill requirements
  - `UserJobMatchRelationship`: Job compatibility scores
- **Composite Models**:
  - `UserRepository`: Complete user profile
  - `CompanyRepository`: Complete company profile
  - `JobMatch`: Job matching results
- **Enums**:
  - `SkillCategory`, `ProficiencyLevel`, `CompanySize`, `ImportanceLevel`, `RequirementType`

#### Agent System (`src/agents/`)
```
src/agents/
├── __init__.py
├── base_agent.py              # Base agent class (placeholder)
├── user_repository_agent.py   # User data collection and analysis
├── job_discovery_agent.py     # Autonomous job discovery and matching
├── resume_generation_agent.py # AI resume generation and optimization
├── job_application_agent.py   # Job application submission handling
└── company_repository_agent.py # Company intelligence gathering
```

**user_repository_agent.py** - User Data Management Agent
- **Classes**:
  - `UserRepositoryAgent`: CrewAI agent for user data management
- **Methods**:
  - `analyze_social_profile()`: Extract data from social media profiles
  - `parse_document()`: Process uploaded documents (resumes, portfolios)
  - `build_user_knowledge_graph()`: Construct user knowledge graph
  - `recommend_baseline_improvements()`: Suggest profile enhancements
- **Purpose**: Collects and analyzes user professional data from multiple sources

**job_discovery_agent.py** - Job Discovery & Matching Agent
- **Classes**:
  - `JobDiscoveryAgent`: CrewAI agent for job discovery
- **Methods**:
  - `monitor_job_boards()`: Scan multiple job boards for opportunities
  - `calculate_job_match_score()`: Calculate user-job compatibility
  - `create_job_notification()`: Generate job opportunity notifications
  - `_scrape_job_source()`: Source-specific job scraping
  - `_calculate_skill_match()`: Skill compatibility scoring
  - `_calculate_experience_match()`: Experience level matching
- **Purpose**: Continuously monitors job markets and identifies relevant opportunities

**resume_generation_agent.py** - Resume Generation Agent
- **Classes**:
  - `ResumeGenerationAgent`: CrewAI agent for resume creation
- **Methods**:
  - `generate_tailored_resume()`: Create job-specific resumes
  - `optimize_for_ats()`: Optimize for applicant tracking systems
  - `calculate_skill_match()`: Analyze skill alignment
  - `select_relevant_experiences()`: Choose most relevant work history
- **Purpose**: Generates tailored, ATS-optimized resumes using knowledge graph data

**job_application_agent.py** - Application Submission Agent
- **Classes**:
  - `JobApplicationAgent`: CrewAI agent for job applications
- **Methods**:
  - `apply_to_job()`: Submit applications via multiple channels
  - `_apply_via_platform()`: Apply through internal platform
  - `_apply_via_linkedin()`: LinkedIn automation
  - `_apply_via_indeed()`: Indeed automation
  - `_apply_via_email()`: Email-based applications
  - `track_application_status()`: Monitor application progress
- **Purpose**: Handles job application submission across different platforms

#### Service Layer (`src/services/`)
```
src/services/
├── __init__.py
├── knowledge_graph_service.py    # High-level knowledge graph operations
├── application_workflow_service.py # Application generation workflow
├── job_monitoring_service.py     # Continuous job monitoring
└── notification_service.py       # User notification management
```

**knowledge_graph_service.py** - Knowledge Graph Service
- **Classes**:
  - `KnowledgeGraphService`: High-level graph operations
- **Methods**:
  - `create_user_repository()`: Initialize user knowledge graph
  - `add_user_skill()`: Add skills to user profile
  - `add_user_experience()`: Add work experience
  - `create_company_repository()`: Initialize company knowledge graph
  - `add_job_posting()`: Add job opportunities
  - `get_user_repository()`: Retrieve complete user profile
  - `calculate_job_compatibility()`: Calculate job match scores
  - `find_skill_gaps()`: Identify missing skills for jobs
- **Purpose**: Provides high-level interface for knowledge graph operations

**application_workflow_service.py** - Application Workflow Orchestration
- **Classes**:
  - `ApplicationWorkflowService`: Workflow orchestration
- **Enums**:
  - `WorkflowStatus`: Workflow state enumeration
- **Methods**:
  - `start_application_workflow()`: Initialize application generation
  - `_execute_workflow()`: Execute workflow steps
  - `_generate_resume()`: Resume generation step
  - `_generate_cover_letter()`: Cover letter generation step
  - `_calculate_ats_score()`: ATS compatibility scoring
  - `approve_application_for_submission()`: User approval handling
  - `_submit_application()`: Application submission step
- **Purpose**: Orchestrates the complete job application workflow from discovery to submission

**job_monitoring_service.py** - Job Monitoring Service
- **Classes**:
  - `JobMonitoringService`: Continuous job monitoring
- **Methods**:
  - `start_monitoring()`: Start background job monitoring
  - `_monitoring_loop()`: Main monitoring loop
  - `_scan_for_jobs()`: Scan for new opportunities
  - `_scan_jobs_for_user()`: User-specific job scanning
  - `enable_monitoring_for_user()`: Enable monitoring for user
  - `get_monitoring_stats()`: Get service statistics
- **Purpose**: Continuously monitors job boards and matches opportunities with users

**notification_service.py** - Notification Management Service
- **Classes**:
  - `NotificationService`: User notification management
- **Enums**:
  - `NotificationType`, `NotificationPriority`: Notification categorization
- **Methods**:
  - `send_job_opportunity_notification()`: Job opportunity alerts
  - `send_application_ready_notification()`: Application ready alerts
  - `send_application_submitted_notification()`: Submission confirmations
  - `handle_notification_action()`: Process user actions on notifications
  - `_send_notification_via_channels()`: Multi-channel notification delivery
- **Purpose**: Manages all user notifications across multiple channels

### Application Entry Point
**run.py** - Development Server
- **Functions**:
  - `main()`: Start development server with configuration
- **Purpose**: Entry point for running the application in development mode

## Data Flow Diagrams

### User Onboarding Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User      │    │   User      │    │ Knowledge   │    │   Neo4j     │
│ Registration│───▶│ Repository  │───▶│   Graph     │───▶│  Database   │
│             │    │   Agent     │    │  Service    │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Social      │    │ Document    │    │ Skill       │    │ User        │
│ Profile     │    │ Analysis    │    │ Extraction  │    │ Knowledge   │
│ Analysis    │    │             │    │             │    │ Graph       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Job Discovery & Application Flow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Job         │    │ Job         │    │ Notification│    │    User     │
│ Monitoring  │───▶│ Discovery   │───▶│  Service    │───▶│ Notification│
│ Service     │    │   Agent     │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Job Board   │    │ Match Score │    │ Job         │    │ Application │
│ Scraping    │    │ Calculation │    │ Opportunity │    │ Workflow    │
│             │    │             │    │ Alert       │    │ Trigger     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Application Generation Workflow
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Application │    │   Resume    │    │ Cover Letter│    │ ATS Scoring │
│ Workflow    │───▶│ Generation  │───▶│ Generation  │───▶│   Agent     │
│ Service     │    │   Agent     │    │   Agent     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ User Review │    │ Application │    │ Job         │    │ Application │
│ & Approval  │───▶│ Submission  │───▶│ Application │───▶│ Tracking    │
│             │    │   Agent     │    │   Agent     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## API Documentation

### Job Monitoring Endpoints

#### Enable Job Monitoring
```http
POST /api/v1/jobs/monitoring/enable?user_id={user_id}
Content-Type: application/json

{
  "preferred_locations": ["San Francisco", "Remote"],
  "preferred_job_types": ["full_time", "contract"],
  "salary_min": 80000,
  "salary_max": 150000,
  "remote_work_preference": "FLEXIBLE",
  "min_match_score": 0.7,
  "max_notifications_per_scan": 5,
  "keywords": ["python", "machine learning", "AI"],
  "excluded_companies": ["Company A", "Company B"]
}
```

#### Get Monitoring Status
```http
GET /api/v1/jobs/monitoring/status?user_id={user_id}

Response:
{
  "monitoring_enabled": true,
  "last_scan": "2024-01-01T12:00:00Z",
  "preferences": {
    "preferred_locations": ["San Francisco", "Remote"],
    "min_match_score": 0.7
  }
}
```

### Health Check
```http
GET /health

Response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Database Schema

### Neo4j Knowledge Graph Schema

#### Node Types
- **USER**: User profile and basic information
- **SKILL**: Technical and soft skills with proficiency levels
- **EXPERIENCE**: Work experience with achievements
- **PROJECT**: User projects demonstrating skills
- **EDUCATION**: Academic background and degrees
- **CERTIFICATION**: Professional certifications
- **COMPANY**: Company profiles and information
- **JOB_POSTING**: Job opportunities with requirements
- **REQUIREMENT**: Specific job requirements and skills needed

#### Relationship Types
- **HAS_SKILL**: User → Skill (with proficiency, years_experience)
- **HAS_EXPERIENCE**: User → Experience
- **USED_SKILL**: Experience → Skill (with frequency, impact)
- **DEMONSTRATES_SKILL**: Project → Skill (with complexity, role)
- **OFFERS_JOB**: Company → Job Posting
- **REQUIRES_SKILL**: Job Posting → Requirement
- **MATCHES_JOB**: User → Job Posting (with compatibility_score)

### PostgreSQL Schema

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);
```

#### Applications Table
```sql
CREATE TABLE applications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    job_posting_id VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    status application_status DEFAULT 'DRAFT',
    ats_score INTEGER,
    match_score INTEGER,
    submitted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## Agent System

The system uses CrewAI agents for intelligent task execution:

### Agent Hierarchy
1. **User Repository Agent**: Collects and analyzes user data
2. **Job Discovery Agent**: Finds and matches job opportunities
3. **Resume Generation Agent**: Creates tailored resumes
4. **Job Application Agent**: Handles application submissions
5. **Company Repository Agent**: Gathers company intelligence

### Agent Communication
Agents communicate through:
- Shared knowledge graph (Neo4j)
- Service layer interfaces
- Event-driven notifications
- Workflow orchestration

## Service Layer

### Service Dependencies
```
Knowledge Graph Service
├── Neo4j Client
└── Knowledge Graph Models

Application Workflow Service
├── Resume Generation Agent
├── Job Application Agent
├── Notification Service
└── Knowledge Graph Service

Job Monitoring Service
├── Job Discovery Agent
├── Notification Service
└── Knowledge Graph Service

Notification Service
├── Email Service
├── Push Notification Service
└── In-App Notification System
```

## Setup & Deployment

### Environment Variables
```bash
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
POSTGRESQL_URL=postgresql://user:pass@localhost/dbname

# API Keys
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key

# Application Settings
DEBUG=true
SECRET_KEY=your_secret_key
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Initialize databases
python -c "from src.database.postgresql_models import init_db; init_db()"

# Start the application
python run.py
```

### Docker Deployment
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - neo4j
      - postgres
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      - POSTGRESQL_URL=postgresql://postgres:password@postgres/jobassistant

  neo4j:
    image: neo4j:5.20.0
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password

  postgres:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=jobassistant
      - POSTGRES_PASSWORD=password
```

This documentation provides a comprehensive overview of the AI Job Application Assistant codebase, including detailed explanations of each component, their interactions, and how they work together to create an intelligent job application system.