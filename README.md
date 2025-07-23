# AI Job Application Assistant

An intelligent platform that automates and optimizes job applications using CrewAI agents and knowledge graphs.

## 🚀 Features

- **User Repository Creation**: Analyzes social media profiles and documents to build comprehensive professional profiles
- **Company Intelligence**: Scrapes company websites and monitors current events to build rich company knowledge bases
- **AI-Generated Applications**: Creates tailored resumes and cover letters using knowledge graph relationships
- **ATS Optimization**: Scores and optimizes applications for Applicant Tracking Systems
- **Project Recommendations**: Suggests targeted projects to fill skill gaps
- **🤖 Autonomous Job Discovery & Application**: Continuously monitors job boards, finds relevant opportunities, and handles the complete application process with minimal human intervention

### 🎯 Auto-Application Workflow

The platform provides a seamless, AI-driven job application experience:

1. **Continuous Monitoring**: AI agents scan multiple job boards (LinkedIn, Indeed, Glassdoor, etc.) every 5 minutes
2. **Smart Matching**: Jobs are scored based on your skills, experience, location, and salary preferences
3. **Instant Notifications**: Get notified about high-match opportunities with a simple "Apply" or "Skip" decision
4. **AI Application Generation**: Upon approval, AI generates tailored resume and cover letter in minutes
5. **Review & Refine**: Review generated materials, make refinements, and approve for submission
6. **Automated Submission**: AI submits applications directly to job boards or company systems
7. **Progress Tracking**: Monitor application status and receive updates automatically

```
🔍 Job Discovery → 📱 User Notification → ✅ User Approval → 🤖 AI Generation → 👀 User Review → 🚀 Auto Submit
```

## 🏗️ Architecture

The system uses a hybrid database approach:
- **Neo4j**: Knowledge graph for complex relationships between users, skills, companies, and jobs
- **PostgreSQL**: User authentication, application tracking, and analytics
- **Pinecone**: Vector database for semantic search and similarity matching
- **Redis**: Caching and session management

## 📁 Project Structure

```
├── src/
│   ├── agents/                 # CrewAI agents
│   │   ├── user_repository_agent.py
│   │   ├── company_repository_agent.py
│   │   └── resume_generation_agent.py
│   ├── api/                    # FastAPI application
│   │   └── main.py
│   ├── config/                 # Configuration management
│   │   └── settings.py
│   ├── database/               # Database clients and models
│   │   ├── neo4j_client.py
│   │   └── postgresql_models.py
│   ├── models/                 # Data models
│   │   └── knowledge_graph.py
│   └── services/               # Business logic
│       └── knowledge_graph_service.py
├── tests/                      # Test files
├── docker-compose.yml          # Local development environment
├── requirements.txt            # Python dependencies
└── run.py                     # Development server
```

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-job-application-assistant
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Start the databases**
   ```bash
   docker-compose up -d
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

## 🔧 Configuration

Key environment variables:

- `OPENAI_API_KEY`: OpenAI API key for AI agents
- `PINECONE_API_KEY`: Pinecone API key for vector database
- `NEO4J_PASSWORD`: Neo4j database password
- `POSTGRESQL_URL`: PostgreSQL connection string

## 🧪 Testing

Run tests with:
```bash
pytest tests/
```

## 📊 Database Access

- **Neo4j Browser**: http://localhost:7474 (neo4j/password)
- **pgAdmin**: http://localhost:8080 (admin@example.com/admin)
- **API Documentation**: http://localhost:8000/docs

## 🤖 CrewAI Agents

The system includes specialized agents:

1. **User Repository Agent**: Collects and analyzes user professional data
2. **Company Repository Agent**: Scrapes company data and job postings
3. **Resume Generation Agent**: Creates tailored resumes
4. **Cover Letter Agent**: Generates personalized cover letters
5. **ATS Scoring Agent**: Evaluates resume compatibility
6. **Project Recommendation Agent**: Suggests skill-building projects
7. **Job Discovery Agent**: Monitors and matches job opportunities

## 🔄 Development Workflow

1. Start with user repository creation
2. Build company intelligence
3. Generate optimized applications
4. Track and analyze performance
5. Iterate based on success metrics

## 📈 Monitoring

The application includes:
- Health check endpoints
- Database connection monitoring
- Application performance tracking
- User analytics and insights

## 🚀 Deployment

For production deployment, see the Kubernetes manifests in the deployment tasks.

## 📝 License

[License information]

## 🤝 Contributing

[Contributing guidelines]