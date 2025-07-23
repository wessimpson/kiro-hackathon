# AI Job Application Assistant - System Diagrams

## System Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[Web Application UI]
        Dashboard[User Dashboard]
        AppManager[Application Manager]
        ProfileBuilder[Profile Builder]
    end

    subgraph "API Gateway"
        FastAPI[FastAPI Server]
        Auth[Authentication]
        CORS[CORS Middleware]
    end

    subgraph "Service Layer"
        KGS[Knowledge Graph Service]
        AWS[Application Workflow Service]
        JMS[Job Monitoring Service]
        NS[Notification Service]
    end

    subgraph "Agent Layer (CrewAI)"
        URA[User Repository Agent]
        JDA[Job Discovery Agent]
        RGA[Resume Generation Agent]
        JAA[Job Application Agent]
        CRA[Company Repository Agent]
    end

    subgraph "Data Layer"
        Neo4j[(Neo4j Knowledge Graph)]
        PostgreSQL[(PostgreSQL)]
        Pinecone[(Pinecone Vector DB)]
        Redis[(Redis Cache)]
    end

    subgraph "External Services"
        OpenAI[OpenAI GPT]
        JobBoards[Job Boards APIs]
        EmailSvc[Email Service]
        WebScraper[Web Scrapers]
    end

    UI --> FastAPI
    Dashboard --> FastAPI
    AppManager --> FastAPI
    ProfileBuilder --> FastAPI

    FastAPI --> KGS
    FastAPI --> AWS
    FastAPI --> JMS
    FastAPI --> NS

    KGS --> URA
    KGS --> Neo4j
    AWS --> RGA
    AWS --> JAA
    JMS --> JDA
    NS --> EmailSvc

    URA --> Neo4j
    JDA --> JobBoards
    JDA --> WebScraper
    RGA --> OpenAI
    JAA --> EmailSvc

    KGS --> PostgreSQL
    AWS --> PostgreSQL
    JMS --> Redis
    NS --> PostgreSQL

    RGA --> Pinecone
    JDA --> Pinecone
```

## Knowledge Graph Schema

```mermaid
erDiagram
    USER {
        string id PK
        string user_id
        string name
        string email
        string location
        string linkedin_url
        string github_url
        datetime created_at
    }

    SKILL {
        string id PK
        string name
        string category
        string proficiency
        int years_of_experience
        datetime last_used
        boolean verified
    }

    EXPERIENCE {
        string id PK
        string company
        string position
        datetime start_date
        datetime end_date
        string description
        array achievements
        boolean is_current
    }

    PROJECT {
        string id PK
        string name
        string description
        array technologies
        string url
        string github_url
        string status
    }

    COMPANY {
        string id PK
        string name
        string industry
        string size
        string website
        string description
        string headquarters
    }

    JOB_POSTING {
        string id PK
        string title
        string description
        string location
        int salary_min
        int salary_max
        datetime posted_date
        string url
        boolean remote_allowed
    }

    REQUIREMENT {
        string id PK
        string skill
        string importance
        int years_required
        string requirement_type
        string description
    }

    USER ||--o{ SKILL : "HAS_SKILL"
    USER ||--o{ EXPERIENCE : "HAS_EXPERIENCE"
    USER ||--o{ PROJECT : "CREATED_PROJECT"
    EXPERIENCE ||--o{ SKILL : "USED_SKILL"
    PROJECT ||--o{ SKILL : "DEMONSTRATES_SKILL"
    COMPANY ||--o{ JOB_POSTING : "OFFERS_JOB"
    JOB_POSTING ||--o{ REQUIREMENT : "REQUIRES_SKILL"
    USER ||--o{ JOB_POSTING : "MATCHES_JOB"
```

## Application Workflow State Machine

```mermaid
stateDiagram-v2
    [*] --> PENDING
    PENDING --> GENERATING_RESUME : Start Workflow
    GENERATING_RESUME --> GENERATING_COVER_LETTER : Resume Complete
    GENERATING_COVER_LETTER --> CALCULATING_ATS_SCORE : Cover Letter Complete
    CALCULATING_ATS_SCORE --> READY_FOR_REVIEW : ATS Score Complete
    READY_FOR_REVIEW --> UNDER_REVIEW : User Opens Review
    UNDER_REVIEW --> READY_FOR_REVIEW : User Requests Changes
    UNDER_REVIEW --> APPROVED_FOR_SUBMISSION : User Approves
    APPROVED_FOR_SUBMISSION --> SUBMITTING : Start Submission
    SUBMITTING --> SUBMITTED : Submission Success
    SUBMITTING --> FAILED : Submission Error
    GENERATING_RESUME --> FAILED : Generation Error
    GENERATING_COVER_LETTER --> FAILED : Generation Error
    CALCULATING_ATS_SCORE --> FAILED : Scoring Error
    FAILED --> [*]
    SUBMITTED --> [*]
```

## Job Discovery Flow

```mermaid
sequenceDiagram
    participant JMS as Job Monitoring Service
    participant JDA as Job Discovery Agent
    participant JobBoards as Job Boards
    participant KGS as Knowledge Graph Service
    participant NS as Notification Service
    participant User as User

    loop Every 5 minutes
        JMS->>JDA: Scan for jobs
        JDA->>JobBoards: Scrape job listings
        JobBoards-->>JDA: Return job data
        
        loop For each user
            JDA->>KGS: Get user profile
            KGS-->>JDA: User skills & preferences
            JDA->>JDA: Calculate match score
            
            alt Match score > threshold
                JDA->>NS: Send job notification
                NS->>User: Job opportunity alert
                User-->>NS: User action (apply/skip/save)
                
                alt User clicks apply
                    NS->>JMS: Trigger application workflow
                end
            end
        end
    end
```

## Resume Generation Process

```mermaid
flowchart TD
    A[Start Resume Generation] --> B[Get User Knowledge Graph]
    B --> C[Get Job Requirements]
    C --> D[Analyze Skill Matches]
    D --> E[Select Relevant Experiences]
    E --> F[Choose Best Projects]
    F --> G[Generate Resume Content]
    G --> H[Optimize for ATS]
    H --> I[Calculate ATS Score]
    I --> J{Score > 70?}
    J -->|Yes| K[Ready for Review]
    J -->|No| L[Generate Improvement Suggestions]
    L --> M[Apply Optimizations]
    M --> H
    K --> N[User Review]
    N --> O{User Approves?}
    O -->|Yes| P[Submit Application]
    O -->|No| Q[Apply User Changes]
    Q --> H
    P --> R[Track Application]
```

## Data Flow Architecture

```mermaid
graph LR
    subgraph "Input Sources"
        LinkedIn[LinkedIn Profile]
        GitHub[GitHub Profile]
        Resume[Resume Upload]
        Portfolio[Portfolio Documents]
    end

    subgraph "Processing Pipeline"
        URA[User Repository Agent]
        NLP[NLP Processing]
        Extraction[Data Extraction]
        Validation[Data Validation]
    end

    subgraph "Knowledge Graph"
        UserNode[User Node]
        SkillNodes[Skill Nodes]
        ExpNodes[Experience Nodes]
        ProjNodes[Project Nodes]
    end

    subgraph "Job Matching"
        JobScraping[Job Scraping]
        MatchCalc[Match Calculation]
        Scoring[ATS Scoring]
        Ranking[Job Ranking]
    end

    subgraph "Application Generation"
        ResumeGen[Resume Generation]
        CoverGen[Cover Letter Generation]
        Optimization[ATS Optimization]
        Review[User Review]
    end

    subgraph "Output"
        Applications[Job Applications]
        Tracking[Application Tracking]
        Analytics[Success Analytics]
    end

    LinkedIn --> URA
    GitHub --> URA
    Resume --> URA
    Portfolio --> URA

    URA --> NLP
    NLP --> Extraction
    Extraction --> Validation
    Validation --> UserNode

    UserNode --> SkillNodes
    UserNode --> ExpNodes
    UserNode --> ProjNodes

    SkillNodes --> MatchCalc
    ExpNodes --> MatchCalc
    JobScraping --> MatchCalc
    MatchCalc --> Scoring
    Scoring --> Ranking

    Ranking --> ResumeGen
    UserNode --> ResumeGen
    ResumeGen --> CoverGen
    CoverGen --> Optimization
    Optimization --> Review

    Review --> Applications
    Applications --> Tracking
    Tracking --> Analytics
```

## Microservices Communication

```mermaid
graph TB
    subgraph "API Gateway"
        Gateway[FastAPI Gateway]
    end

    subgraph "Core Services"
        UserSvc[User Service]
        JobSvc[Job Service]
        AppSvc[Application Service]
        NotifSvc[Notification Service]
    end

    subgraph "AI Services"
        AgentOrch[Agent Orchestrator]
        ResumeAI[Resume AI Service]
        MatchAI[Matching AI Service]
        ATSAI[ATS Scoring AI]
    end

    subgraph "Data Services"
        GraphDB[Graph Database Service]
        RelDB[Relational Database Service]
        VectorDB[Vector Database Service]
        Cache[Cache Service]
    end

    subgraph "External Integrations"
        JobBoards[Job Boards API]
        EmailSvc[Email Service]
        WebhookSvc[Webhook Service]
    end

    Gateway --> UserSvc
    Gateway --> JobSvc
    Gateway --> AppSvc
    Gateway --> NotifSvc

    UserSvc --> GraphDB
    UserSvc --> RelDB
    JobSvc --> AgentOrch
    AppSvc --> ResumeAI
    AppSvc --> ATSAI

    AgentOrch --> MatchAI
    AgentOrch --> JobBoards
    ResumeAI --> VectorDB
    MatchAI --> GraphDB

    NotifSvc --> EmailSvc
    NotifSvc --> WebhookSvc
    
    GraphDB --> Cache
    RelDB --> Cache
```

## Security & Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant Gateway
    participant AuthSvc
    participant UserSvc
    participant Database

    User->>Frontend: Login Request
    Frontend->>Gateway: POST /auth/login
    Gateway->>AuthSvc: Validate Credentials
    AuthSvc->>Database: Check User
    Database-->>AuthSvc: User Data
    AuthSvc-->>Gateway: JWT Token
    Gateway-->>Frontend: Token + User Info
    Frontend-->>User: Login Success

    Note over User,Database: Subsequent API Calls

    User->>Frontend: API Request
    Frontend->>Gateway: Request + JWT Token
    Gateway->>AuthSvc: Validate Token
    AuthSvc-->>Gateway: Token Valid
    Gateway->>UserSvc: Process Request
    UserSvc-->>Gateway: Response
    Gateway-->>Frontend: API Response
    Frontend-->>User: Display Result
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Nginx Load Balancer]
    end

    subgraph "Application Tier"
        App1[FastAPI Instance 1]
        App2[FastAPI Instance 2]
        App3[FastAPI Instance 3]
    end

    subgraph "Background Services"
        JobMonitor[Job Monitoring Service]
        AgentWorker[Agent Worker Pool]
        NotifWorker[Notification Worker]
    end

    subgraph "Database Tier"
        Neo4jCluster[Neo4j Cluster]
        PostgresCluster[PostgreSQL Cluster]
        RedisCluster[Redis Cluster]
        PineconeCloud[Pinecone Cloud]
    end

    subgraph "External Services"
        OpenAIAPI[OpenAI API]
        EmailProvider[Email Provider]
        JobAPIs[Job Board APIs]
    end

    subgraph "Monitoring"
        Prometheus[Prometheus]
        Grafana[Grafana]
        Logs[Centralized Logging]
    end

    LB --> App1
    LB --> App2
    LB --> App3

    App1 --> Neo4jCluster
    App2 --> PostgresCluster
    App3 --> RedisCluster

    JobMonitor --> AgentWorker
    AgentWorker --> OpenAIAPI
    NotifWorker --> EmailProvider

    App1 --> Prometheus
    App2 --> Prometheus
    App3 --> Prometheus
    Prometheus --> Grafana

    JobMonitor --> Logs
    AgentWorker --> Logs
    NotifWorker --> Logs
```

## Error Handling & Recovery

```mermaid
flowchart TD
    A[API Request] --> B{Authentication Valid?}
    B -->|No| C[Return 401 Unauthorized]
    B -->|Yes| D{Rate Limit OK?}
    D -->|No| E[Return 429 Too Many Requests]
    D -->|Yes| F[Process Request]
    F --> G{Service Available?}
    G -->|No| H[Circuit Breaker Open]
    H --> I[Return 503 Service Unavailable]
    G -->|Yes| J[Execute Business Logic]
    J --> K{Database Available?}
    K -->|No| L[Retry with Backoff]
    L --> M{Max Retries Reached?}
    M -->|Yes| N[Return 500 Internal Error]
    M -->|No| K
    K -->|Yes| O[Process Data]
    O --> P{Validation Passed?}
    P -->|No| Q[Return 400 Bad Request]
    P -->|Yes| R[Return Success Response]
    
    N --> S[Log Error]
    I --> S
    C --> S
    E --> S
    Q --> S
    S --> T[Send Alert]
    T --> U[Update Metrics]
```

These diagrams provide a comprehensive visual representation of the AI Job Application Assistant system, showing how all components interact and work together to deliver an intelligent job application automation platform.